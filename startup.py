import os
import sys
import getpass
import base64
import requests


def check_startup(spark_bot=True):

    startup_vars = {}
    write_sparkToken = False

    print('Checking to see if startup.cfg has the required settings...')

    if ('primeServer' and 'primeAuthToken') in os.environ:
        server = os.environ.get('primeServer')
        primeAuthToken = os.environ.get('primeAuthToken')
        print('From OS environ: server=', server)
        print('From OS environ: primeAuthToken=', primeAuthToken)

    if 'sparkBotToken' in os.environ:
        sparkBotToken = os.environ.get('sparkBotToken')
        print('From OS environ: Spark Bot Token=', sparkBotToken, '\n')

    f = open('startup.cfg', 'r')
    f.readline()
    for line in f:
        newline = line.split("=", 1)
        if (newline[0].strip() == "server") and not('primeServer' in os.environ):
            server = newline[1].strip()
            print('From startup.cfg: server=', server)
        elif (newline[0].strip() == "primeAuthToken") and not('primeAuthToken' in os.environ):
            primeAuthToken = newline[1].strip()
            print('From startup.cfg: primeAuthToken=', primeAuthToken)
        elif (newline[0].strip() == "sparkBotToken") and not('sparkBotToken' in os.environ):
            sparkBotToken = newline[1].strip()
            print('From startup.cfg: Spark Bot Token=', sparkBotToken)
        elif (newline[0].strip() == "allowed_domain"):
            allowed_domain = newline[1].strip()
            print('From startup.cfg: allowed_domain=', allowed_domain,)
        elif (newline[0].strip() == "allowed_email"):
            allowed_email = newline[1].strip()
            print('From startup.cfg: allowed_email=', allowed_email)

            break

    print('\n')

    if (server == '' or primeAuthToken == ''):
        if (server == ''):
            server = input('Enter the Prime Instructure Server IP Address:')
        if (primeAuthToken == ''):
            print('Enter your Prime NB API username and password to generate your Basic Auth token.')
            userId = input('Username:')
            passwd = getpass.getpass()
            userPass = userId + ':' + passwd
            base64Val = base64.b64encode(userPass.encode())
            primeAuthToken = base64Val.decode()
            print('Your Base64 Encoded token is = {}\n\n'.format(primeAuthToken))

        with open('startup.cfg', 'r') as file:
            data = file.readlines()

        for line in data:
            newline = line.split("=", 1)
            if newline[0].strip() == "server":
                data[data.index(line)] = 'server = {}\n'.format(server)
            elif newline[0].strip() == "primeAuthToken":
                data[data.index(line)] = 'primeAuthToken = {}\n'.format(primeAuthToken)

        print('Prime: Contents to be written to startup.cfg:{}\n\n'.format(data))

        with open('startup.cfg', 'w') as file:
            file.writelines(data)

    if sparkBotToken == '':
        write_sparkToken = True
        spark_bot = input('Do you want to enable the Spark bot interface?\nEnter [Y]es to enable or [N]o to disable:')
        if spark_bot.lower() == 'y':
            spark_bot = True
            print("Enter the token for your Spark Bot. \n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.ciscospark.com/apps.html "
                  "URL and generate a new access token.")
            sparkBotToken = input('sparkBotToken:')
        else:
            spark_bot = False
            sparkBotToken = 'Disable'

    if write_sparkToken:
        with open('startup.cfg', 'r') as file:
            data = file.readlines()

        for line in data:
            newline = line.split("=", 1)
            if newline[0].strip() == "sparkBotToken":
                data[data.index(line)] = 'sparkBotToken = {}\n'.format(sparkBotToken)

        print('Spark: Contents to be written to startup.cfg:{}\n\n'.format(data))

        with open('startup.cfg', 'w') as file:
            file.writelines(data)

    headers = {
        "authorization": "Basic " + primeAuthToken,
        "accept": "application/json",
        "content-type": "application/json"
    }

    url = 'https://' + server + '/webacs/api/v1/op/info/version'

    print('Trying connection to Prime server : {} ...'.format(server))
    try:
        resp = requests.get(url, headers=headers, timeout=25, verify=False)
        resp.raise_for_status()
    except requests.exceptions.Timeout as err:
        print('\n', err)
        print('Prime server appears to be unreachable!!')
        sys.exit(1)
    except requests.exceptions.HTTPError as err:
        print('\n', err)
        if resp.status_code == 401:
            print("Looks like your token is invalid. \n"
                  "Ensure you used the correct username and password.\n"
                  "Run getToken.py to generate a new token and update it in startup.cfg.\n\n")
            sys.exit()
        else:
            print('HTTPError: Check error code', resp.status_code)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print('\n', err)
        print('RequestException')
        sys.exit(1)

    if resp.status_code == 200:
        print('Status code={}. Making calls to Prime server: {}\n'.format(resp.status_code, server))

    if spark_bot :
        if sparkBotToken.lower() != 'disable' :
            url = 'https://api.ciscospark.com/v1/people/me'
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "Bearer " + sparkBotToken
            }

            print('Connecting to Spark Cloud Service...')
            try:
                resp = requests.get(url, headers=headers, timeout=25, verify=False)
                resp.raise_for_status()
            except requests.exceptions.Timeout as err:
                print('\n', err)
                print('Spark service appears to be unreachable!!')
                sys.exit(1)
            except requests.exceptions.HTTPError as err:
                print('\n', err)
                if resp.status_code == 401:
                    print("Looks like provided Spark Bot access token is not correct. \n"
                          "Please review it and make sure it belongs to your bot account.\n"
                          "Do not worry if you have lost the access token. "
                          "You can always go to https://developer.ciscospark.com/apps.html "
                          "URL and generate a new access token.")
                else:
                    print('HTTPError: Check error code', resp.status_code)
                sys.exit(1)
            except requests.exceptions.RequestException as err:
                print('\n', err)
                print('RequestException')
                sys.exit(1)

            if resp.status_code == 200:
                response_json = resp.json()
                bot_name = response_json['displayName']
                bot_email = response_json['emails'][0]
                print('Status code={}.\nResponse={}\n'.format(resp.status_code, response_json))

            if "@sparkbot.io" not in bot_email:
                print("You have provided access token which does not belong to your bot.\n"
                      "Please review it and make sure it belongs to your bot account.\n"
                      "Do not worry if you have lost the access token. "
                      "You can always go to https://developer.ciscospark.com/apps.html "
                      "URL and generate a new access token.\n\n")
                sys.exit()

            startup_vars['sparkBotToken'] = sparkBotToken
            startup_vars['bot_name'] = bot_name
            startup_vars['bot_email'] = bot_email
            startup_vars['allowed_domain'] = allowed_domain
            startup_vars['allowed_email'] = allowed_email

    startup_vars['server'] = server
    startup_vars['primeAuthToken'] = primeAuthToken

    return startup_vars