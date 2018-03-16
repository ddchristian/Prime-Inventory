import subprocess
import os
import platform
import socket
import time
import atexit
import psutil
import requests
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from startup import check_startup
from queryMethods import getDevice


def is_running(process):

    if platform.system() == "Linux":
        s = subprocess.Popen(['ps', 'axw'], stdout = subprocess.PIPE)

        if process in str(s.stdout.readlines()) :
            return True
        else:
            return False

    elif platform.system() == "Windows":

        if process + ".exe" in (p.name() for p in psutil.process_iter()):
            return True
        else:
            return False



def kill_ngrok():

    if platform.system() == "Linux":
        p = subprocess.Popen(['pkill', '-f', 'ngrok'])
        print(str(p.stdout))

    elif platform.system() == "Windows":
        for p in psutil.process_iter():
            if p.name() == 'ngrok.exe':
                subprocess.Popen("taskkill /F /T /PID %i"%p.pid, shell=True)

    print('Killed ngrok process on exit!')


def check_webhook():

    url = URL + '/webhooks'

    ngrok_url = requests.get(
        "http://127.0.0.1:4040/api/tunnels", headers={"Content-Type": "application/json"}).json()

    print('ngrok_url_json is:', ngrok_url)

    for urls in ngrok_url["tunnels"]:
        if "https://" in urls['public_url']:
            target_url = urls['public_url']
            address = urls['config']['addr']
            print('Ngrok target_url is:', target_url)
            print('Ngrok address is:', address)

    webhook_js = send_spark_get(url, js=True)
    print('webhook_js initial check is: ', webhook_js)

    items = webhook_js['items']

    if len(items) > 0 :
        print(items)
        for webhook in range(len(items)) :
            if ((items[webhook]['name'] == webhook_name) and (items[webhook]['resource'] in resources)):
                print('Webhook name =', items[webhook]['name'])
                print('resource =', items[webhook]['resource'] )
                send_spark_delete(url + '/' + items[webhook]['id'])


    for webhook in resources :
        payload = {'name': webhook_name, 'targetUrl': target_url + bot_route, 'resource' : webhook, 'event' : event}
        webhook_js = send_spark_post(url, data=payload, js=True)
        print(webhook_js)

    return


def send_spark_get(url, payload=None, js=True):

    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_spark_delete(url, js=False):

  request = requests.delete(url, headers=headers)
  if js != False:
    request = request.json()
  return request


def send_spark_post(url, data, js=True):

  request = requests.post(url, json.dumps(data), headers=headers)
  if js:
    request = request.json()
  return request


def help():
    return "Sure! I can help. Below are the commands that I understand:<br/>" \
            "`Help` - I will display what I can do.<br/>" \
            "`Hello` - I will display my greeting message<br/>" \
            "`Serial [serial number]` - I will search for a serial number in Prime database <br/>" \
            "`IP [IP Address]` - I will search for an IP Address in Prime database <br/>" \
            "`nmac [mac address]` - I will search for a **network** mac address in Prime database <br/>" \
            "`cmac [mac address]` - I will search for a **client** mac address in Prime database <br/>"


def hello():
    return "Hi my name is %s bot.<br/>" \
           "Type `Help` to see what I can do.<br/>" % bot_name


def get_serial(searchValue):
    result = getDevice(startup_vars, 'serialNumberQ', searchValue, '')

    if not result :
        result_msg = 'Nothing returned from search. Item %s not found in Prime database.<br/>' % searchValue

    else:
        result_msg = 'Summary details for search with Serial Number: %s !<br/>' % searchValue
        for key, value in result.items() :
            result_msg += (key + ' : ' + value + '<br/>')

    print(result_msg)

    return result_msg


def get_ip(searchValue):
    result = getDevice(startup_vars, 'ipAddrQ', searchValue, '')

    if not result :
        result_msg = 'Nothing returned from search. Item %s not found in Prime database.<br/>' % searchValue

    else:
        result_msg = 'Summary details for search with IP Address: %s !<br/>' % searchValue
        for key, value in result.items() :
            result_msg += (key + ' : ' + value + '<br/>')

    print(result_msg)

    return result_msg



def get_nmac(searchValue):
    result = getDevice(startup_vars, 'macAddrQ', searchValue, 'network')

    if not result :
        result_msg = 'Nothing returned from search. Item %s not found in Prime database.<br/>' % searchValue

    else:
        result_msg = 'Summary details for search with mac address: %s !<br/>' % searchValue
        for key, value in result.items() :
            result_msg += (key + ' : ' + value + '<br/>')

    print(result_msg)

    return result_msg


def get_cmac(searchValue):
    result = getDevice(startup_vars, 'macAddrQ', searchValue, 'client')

    if not result :
        result_msg = 'Nothing returned from search. Item %s not found in Prime database.<br/>' % searchValue

    else:
        result_msg = 'Summary details for search with mac address: %s !<br/>' % searchValue
        for key, value in result.items() :
            result_msg += (key + ' : ' + value + '<br/>')

    print(result_msg)

    return result_msg

def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_addr = s.getsockname()[0]
    response = requests.get('https://httpbin.org/ip')
    public_addr = response.json()['origin']
    result_msg = 'Local ip address = {}<br/> Public ip address = {}<br/>'.format(local_addr, public_addr)

    print(result_msg)

    return result_msg


def allowed_user(user_email):
    if user_email in allowed_email or user_email.split('@')[1] in allowed_domain or allowed_domain[0]=='*':
        return True
    elif '@sparkbot.io' in user_email:
        return True
    else:
        print('user_email={} is not in the approved list. Exiting request processing!'.format(user_email))
        return False


app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('search'))


@app.route('/bot', methods=['GET', 'POST'])
def bot():
    if request.method == 'GET':
        print('Hello bot get request')
        return '<br/><br/>Prime Quick Search Bot is up and running. @mention QPrime from Spark <strong>@QPrime help</strong> to start!'


    elif request.method == 'POST':
        webhook = request.get_json()
        #print(webhook)

        resource = webhook['resource']
        senders_email = webhook['data']['personEmail']
        room_id = webhook['data']['roomId']

        if senders_email != bot_email:
            print(webhook)
        if resource == "memberships" and senders_email == bot_email:
            print(webhook)
            send_spark_post("https://api.ciscospark.com/v1/messages",
                            {
                                "roomId": room_id,
                                "markdown": (hello() +
                                             "**Note: This is a group room and you have to call "
                                             "me specifically with `@%s` for me to respond.**" % bot_name)
                            }
                            )


        if  allowed_user(webhook['data']['personEmail']):
            if ("@sparkbot.io" not in webhook['data']['personEmail']):
                print('Requester email= ', webhook['data']['personEmail'])
                print('msgID= ', webhook['data']['id'])
                result = send_spark_get(
                    'https://api.ciscospark.com/v1/messages/{}'.format(webhook['data']['id']))
                print('Raw request=', result['text'])
                message = result['text'].lower()
                message = message.replace(bot_name.lower(), '').strip()
                print('Parsed request=', message)
                if message.startswith('help'):
                    msg = help()
                elif message.startswith('hello'):
                    msg = hello()
                elif message.startswith('serial'):
                    message = message.replace('serial', '')
                    if message == '' :
                        msg = "Please enter request in format: @{} serial [serial number]".format(bot_name)
                    else:
                        msg = get_serial(message.strip().upper())

                elif message.startswith('ip'):
                    message = message.replace('ip', '')
                    if message == '' :
                        msg = "Please enter request in format: @{} ip [IP Address]".format(bot_name)
                    else:
                        msg = get_ip(message.strip().upper())

                elif message.startswith('network'):
                    message = message.replace('network', '')
                    if message == '' :
                        msg = "Please enter request in format: @{} network [network mac address]".format(bot_name)
                    else:
                        msg = get_nmac(message.strip().upper())

                elif message.startswith('client'):
                    message = message.replace('client', '')
                    if message == '' :
                        msg = "Please enter request in format: @{} client [client mac address]".format(bot_name)
                    else:
                        msg = get_cmac(message.strip().upper())

                elif message.startswith('hostip') or message.startswith('host'):
                        msg = get_host()
                else:
                    msg = "Sorry, but I did not understand your request. Type `Help` to see what I can do"

                if msg != None:
                    send_spark_post("https://api.ciscospark.com/v1/messages",
                                    {"roomId": webhook['data']['roomId'], "markdown": msg})

        return "true"

@app.route('/search', methods =['GET', 'POST'])
def search():
    if request.method == 'GET' :
        return render_template("form_submit.html")
    else:
        searchOptions = {'macAddrQ' : 'mac', 'deviceTypeQ' : 'device', 'softwareQ' : 'software' }
        queryType = {'serialNumberQ' : 'Serial Number', 'ipAddrQ': 'IP Address' , 'macAddrQ': 'MAC Address', 'deviceTypeQ': 'Device Type', 'softwareQ': 'Software Type'}
        option =''
        query = request.form['query']
        print('Query=', query)
        if query != 'softwareQ':
            searchValue = request.form['searchValue'].upper().strip()
        else:
            searchValue = ''
        if (query in searchOptions) :
            option = request.form[searchOptions[query]]
        print('queryType =', queryType)
        print('searchValue =', searchValue)
        print('option =', option)
        result = getDevice(startup_vars, query, searchValue, option)
        print('result=', result)
        if query in ['softwareQ', 'deviceTypeQ'] :
           print('queryType[query]=', queryType[query])
           print('searchValue=,', searchValue)
           print('option=', option)
           #print(' queryType = queryType[query], searchValue=searchValue, option=option, result=result)')
           return render_template('device_action_list.html', queryType = queryType[query], searchValue=searchValue, option=option, result=result)
        return render_template('device_action.html', queryType = queryType[query], searchValue=searchValue, option=option, result=result)

if __name__ == "__main__" :

    flask_port = 5050

    startup_vars = check_startup()
    print('From __main__: startup_vars=', startup_vars)

    if 'sparkBotToken' in startup_vars:
        sparkBotToken = startup_vars['sparkBotToken']
        bot_name = startup_vars['bot_name']
        bot_email = startup_vars['bot_email']
        allowed_domain = startup_vars['allowed_domain']
        allowed_email = startup_vars['allowed_email']
        del startup_vars['sparkBotToken']
        del startup_vars['bot_name']
        del startup_vars['allowed_domain']
        del startup_vars['allowed_email']
        URL = "https://api.ciscospark.com/v1"
        webhook_name = 'prime_query'
        resources = ['messages', 'memberships']
        event = 'created'
        bot_route = '/bot'

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + sparkBotToken
        }

        allowed_domain = [element.strip() for element in allowed_domain.split(',')]
        print('allowed_domain=', allowed_domain)
        allowed_email = [element.strip() for element in allowed_email.split(',')]
        print('allowed_email=', allowed_email)


        if is_running('ngrok'):
            print('Ngrok is running... Checking Spark webhook')
            check_webhook()

        else:

            print('Starting up set process')

            if platform.system() != "Windows":
                ngrok_run = subprocess.Popen(
                    ["ngrok http " + str(flask_port)], shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)
                print('ngrok pid =', ngrok_run.pid)

            elif platform.system() == "Windows":
                ngrok_run = os.popen("ngrok http " + str(flask_port), mode='r', buffering=-1)

            time.sleep(2)
            check_webhook()


    print('\n********   Starting up Flask Web...    ********\n\n')

    app.run(host='0.0.0.0', port=flask_port)

    atexit.register(kill_ngrok)
