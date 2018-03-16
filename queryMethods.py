import requests
import json
from collections import OrderedDict


def getJSON (query, searchValue, option) :

    baseApi = '/webacs/api/v1/data'
    filter = '''/InventoryDetails?.full=true&.sort=summary.deviceName&.or_filter=true&udiDetail.udiSerialNr="{}"&powerSupply.serialNumber="{}"'''
    udiFilter = '/InventoryDetails?.full=true&.sort=summary.deviceName&udiDetail.udiSerialNr='
    powerFilter = '/InventoryDetails?.full=true&.sort=summary.deviceName&powerSupply.serialNumber='
    ipAddrFilter = '/InventoryDetails?.full=true&.sort=summary.deviceName&ipInterface.ipAddress='
    clientIPFilter = '/ClientDetails?.full=true&ipAddress="%s"'
    networkMacFilter = '/InventoryDetails?.full=true&.sort=summary.deviceName&ethernetInterface.macAddress='
    clientMacFilter = '/ClientDetails?.full=true&macAddress='
    deviceFilter = '/InventoryDetails?.full=true&.sort=summary.deviceName&udiDetail.modelNr='
    softwareFilter = '/Devices?.full=true&softwareType='
    apFilter = '/AccessPointDetails?.full=true&serialNumber='
    #apEtherMac = '/AccessPointDetails?.full=true&ethernetMac='
    #apMac ='/AccessPointDetails?.full=true&macAddress='
    apMac = '/AccessPointDetails?.full=true&.or_filter=true&ethernetMac="%s"&macAddress="%s"'
    apIpAddrFilter = '/AccessPointDetails?.full=true&ipAddress='
    apDeviceFilter = '/AccessPointDetails?.full=true&model='


    headers = {
        "authorization": "Basic " + token ,
        "accept": "application/json",
        "content-type": "application/json"
    }
    

    print('Headers is: ', headers)

    call = ''
    response_json = 'none'

    if query == 'serialNumberQ':

        url = 'https://' + server + baseApi + apFilter + '"' + searchValue + '"'
        print('url is: ', url)

        resp = requests.get(url, headers=headers, verify=False)
        response_json = resp.json()  # Get the json-encoded content from response
        print("Status: ", resp.status_code)  # This is the http request status
        print(json.dumps(response_json,
                         indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

        if (response_json['queryResponse']['@count'] == '1'):
            call = 'ap'

        else:
            url = 'https://' + server + baseApi + filter.format(searchValue, searchValue)
            #url = 'https://' + server + baseApi + udiFilter + '"' + searchValue + '"'
            print('url is: ', url)

            resp = requests.get(url, headers=headers, verify=False)
            response_json = resp.json()  # Get the json-encoded content from response
            print("Status: ", resp.status_code)  # This is the http request status
            print(json.dumps(response_json,
                             indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

            if (response_json['queryResponse']['@count'] > '0'):
                call = 'udi'

            else:
                url = 'https://' + server + baseApi + powerFilter + '"' + searchValue + '"'
                print('url is: ', url)

                resp = requests.get(url, headers=headers, verify=False)
                response_json = resp.json()  # Get the json-encoded content from response
                print("Status: ", resp.status_code)  # This is the http request status
                print(json.dumps(response_json,
                                 indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

                if (response_json['queryResponse']['@count'] == '1'):
                    call = 'power'

    elif query == 'ipAddrQ' :

        url = 'https://' + server + baseApi + apIpAddrFilter + '"' + searchValue + '"'
        print('url is: ', url)

        resp = requests.get(url, headers=headers, verify=False)
        response_json = resp.json()  # Get the json-encoded content from response
        print("Status: ", resp.status_code)  # This is the http request status
        print(json.dumps(response_json,
                         indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

        if (response_json['queryResponse']['@count'] == '1'):
            api = apIpAddrFilter
            call = 'ap'

        else:
            url = 'https://' + server + baseApi + ipAddrFilter + 'startsWith(%s)' %(searchValue)
            print('url is: ', url)

            resp = requests.get(url, headers=headers, verify=False)
            response_json = resp.json()  # Get the json-encoded content from response
            print("Status: ", resp.status_code)  # This is the http request status
            print(json.dumps(response_json,
                             indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

            if (response_json['queryResponse']['@count'] == '1'):
                api = ipAddrFilter
                call = 'ipAddr'


            else:
                url = 'https://' + server + baseApi + clientIPFilter  %(searchValue)
                print('url is: ', url)

                resp = requests.get(url, headers=headers, verify=False)
                response_json = resp.json()  # Get the json-encoded content from response
                print("Status: ", resp.status_code)  # This is the http request status
                print(json.dumps(response_json,
                                 indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

                if (response_json['queryResponse']['@count'] == '1'):
                    api = clientIPFilter
                    call = 'client'

    elif query == 'macAddrQ' :
        if option == 'network' :


            url = 'https://' + server + baseApi + apMac  %(searchValue, searchValue)
            print('url is: ', url)

            resp = requests.get(url, headers=headers, verify=False)
            response_json = resp.json()  # Get the json-encoded content from response
            print("Status: ", resp.status_code)  # This is the http request status
            print(json.dumps(response_json,
                             indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

            if (response_json['queryResponse']['@count'] == '1'):
                api = apMac
                call = 'ap'

            else:

                url = 'https://' + server + baseApi + networkMacFilter + '"' + searchValue + '"'
                print('url is: ', url)

                resp = requests.get(url, headers=headers, verify=False)
                response_json = resp.json()  # Get the json-encoded content from response
                print("Status: ", resp.status_code)  # This is the http request status
                print(json.dumps(response_json,
                                 indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

                if (response_json['queryResponse']['@count'] == '1'):
                    api = networkMacFilter
                    call = 'networkMAC'
        else:
            url = 'https://' + server + baseApi + clientMacFilter + '"' + searchValue + '"'
            print('url is: ', url)

            resp = requests.get(url, headers=headers, verify=False)
            response_json = resp.json()  # Get the json-encoded content from response
            print("Status: ", resp.status_code)  # This is the http request status
            print(json.dumps(response_json,
                             indent=4))  # Convert "response_json" object to a JSON formatted string and print it out

            if (response_json['queryResponse']['@count'] == '1'):
                api = clientMacFilter
                call = 'client'

    elif query == 'deviceTypeQ' :
        url = 'https://' + server + baseApi + deviceFilter + option + '(' +  '"' +  searchValue +  '"' +')'
        print('url is: ', url)

        resp = requests.get(url, headers=headers, verify=False)
        response_json = resp.json()  # Get the json-encoded content from response
        print("Status: ", resp.status_code)  # This is the http request status
        print(json.dumps(response_json,
                         indent=4))  # Convert "response_json" object to a JSON formatted string and print it out
        call = 'device'

    elif query == 'softwareQ' :
        url = 'https://' + server + baseApi + softwareFilter + '"' + option + '"'
        print('url is: ', url)

        resp = requests.get(url, headers=headers, verify=False)
        response_json = resp.json()  # Get the json-encoded content from response
        print("Status: ", resp.status_code)  # This is the http request status
        print(json.dumps(response_json,
                         indent=4))  # Convert "response_json" object to a JSON formatted string and print it out
        call = 'software'

    print('call is: ', call)
    print('@count from json call is: ',response_json['queryResponse']['@count'])

    return [call, response_json]


def getDevice (startup_vars, query, searchValue, option) :
    global server, token
    server = startup_vars['server']
    token = startup_vars['primeAuthToken']

    results = OrderedDict()
    [call, response_json] = getJSON(query, searchValue, option)


    if call == 'udi' :
        device = response_json['queryResponse']['entity'][0]['inventoryDetailsDTO']
        summary = device['summary']
        udiDetail = device['udiDetails']['udiDetail']
        powerDetail = device['powerSupplies']['powerSupply']
        displayName = device['@displayName']

        results['deviceType'] = summary['deviceType']
        results['deviceName'] = summary['deviceName']
        results['ipAddress'] = summary['ipAddress']
        results['reachability'] = summary['reachability']
        results['softwareVersion'] = summary['softwareVersion']

        if summary['locationCapable'] :
            if 'location' in summary:
                results['location'] = summary['location']
            if 'contact' in summary:
                results['contact'] = summary['contact']

        for i in range(len(udiDetail)):
            if ('udiSerialNr' in udiDetail[i]) and (udiDetail[i]['udiSerialNr'] == searchValue) :
                results["description"] = udiDetail[i]['description']
                results['name'] = udiDetail[i]['name']
                results['modelNr'] = udiDetail[i]['modelNr']
                results['productId'] = udiDetail[i]['productId']
                results['udiSerialNr'] = udiDetail[i]['udiSerialNr']


        if isinstance(powerDetail, list) :
            for i in range(len(powerDetail)):
                if ('serialNumber' in powerDetail[i]) and (powerDetail[i]['serialNumber'] == searchValue) :
                    results["description"] = powerDetail[i]['description']
                    results['name'] = powerDetail[i]['name']
                    results['serialNumber'] = powerDetail[i]['serialNumber']
                    results['operationalStatus'] = powerDetail[i]['operationalStatus']


        elif isinstance(powerDetail, dict) :
            if ('serialNumber' in powerDetail) and (powerDetail['serialNumber'] == searchValue):
                results["description"] = powerDetail['description']
                results['name'] = powerDetail['name']
                results['serialNumber'] = powerDetail['serialNumber']
                results['operationalStatus'] = powerDetail['operationalStatus']

    elif call == 'power' :
        device = response_json['queryResponse']['entity'][0]['inventoryDetailsDTO']
        powerDetail = device['powerSupplies']['powerSupply']
        summary = device['summary']
        displayName = device['@displayName']

        if isinstance(powerDetail, list) :
            for i in range(len(powerDetail)):
                if ('serialNumber' in powerDetail[i]) and (powerDetail[i]['serialNumber'] == searchValue) :
                    results["description"] = powerDetail[i]['description']
                    results['name'] = powerDetail[i]['name']
                    results['serialNumber'] = powerDetail[i]['serialNumber']
                    results['operationalStatus'] = powerDetail[i]['operationalStatus']
                    results['deviceType'] = summary['deviceType']
                    results['deviceName'] = summary['deviceName']
                    results['ipAddress'] = summary['ipAddress']

        elif isinstance(powerDetail, dict) :
            results["description"] = powerDetail['description']
            results['name'] = powerDetail['name']
            results['serialNumber'] = powerDetail['serialNumber']
            results['operationalStatus'] = powerDetail['operationalStatus']
            results['deviceType'] = summary['deviceType']
            results['deviceName'] = summary['deviceName']
            results['ipAddress'] = summary['ipAddress']

    elif call == 'ap' :
        device = response_json['queryResponse']['entity'][0]['accessPointDetailsDTO']
        print('Device is: ',device)
        results["description"] = 'Unified Access Point'
        results['name'] = device['name']
        results['model'] = device['model']
        results['serialNumber'] = device['serialNumber']
        results['ipAddress'] = device['ipAddress']
        results['macAddress'] = device['macAddress']
        results['ethernetMac'] = device['ethernetMac']
        results['reachabilityStatus'] = device['reachabilityStatus']
        results['locationHeirarchy'] = device['locationHeirarchy']
        results['controllerName'] = device['unifiedApInfo']['controllerName']
        results['controllerIpAddress'] = device['unifiedApInfo']['controllerIpAddress']
        results['softwareVersion'] = device['softwareVersion']
        print('Type device[cdpNeighbors][cdpNeighbor]', type(device['cdpNeighbors']['cdpNeighbor']))
        if isinstance(device['cdpNeighbors']['cdpNeighbor'], dict) :
            results['neighborName'] = device['cdpNeighbors']['cdpNeighbor']['neighborName']
            results['neighborIpAddress'] = device['cdpNeighbors']['cdpNeighbor']['neighborIpAddress']
            results['neighborPort'] = device['cdpNeighbors']['cdpNeighbor']['neighborPort']

    elif call == 'ipAddr' :
        device = response_json['queryResponse']['entity'][0]['inventoryDetailsDTO']
        ipAddrDetail = device['ipInterfaces']['ipInterface']
        summary = device['summary']
        displayName = device['@displayName']
        for i in range(len(ipAddrDetail)):
            searchIP = ipAddrDetail[i]['ipAddress'].split('/')
            if (searchIP[0] == searchValue) :
                results["ipAddress"] = ipAddrDetail[i]['ipAddress']
                results['name'] = ipAddrDetail[i]['name']
                results['adminStatus'] = ipAddrDetail[i]['adminStatus']
                results['operationalStatus'] = ipAddrDetail[i]['operationalStatus']
                results['deviceType'] = summary['deviceType']
                results['deviceName'] = summary['deviceName']
                results['Chassis_ipAddress'] = summary['ipAddress']

    elif call == 'networkMAC' :
        print('networkMAC')
        device = response_json['queryResponse']['entity'][0]['inventoryDetailsDTO']
        macAddrDetail = device['ethernetInterfaces']['ethernetInterface']
        summary = device['summary']
        displayName = device['@displayName']
        for i in range(len(macAddrDetail)):
            if (macAddrDetail[i]['macAddress'].upper() == searchValue) :
                results["macAddress"] = macAddrDetail[i]['macAddress']
                results['name'] = macAddrDetail[i]['name']
                results['adminStatus'] = macAddrDetail[i]['adminStatus']
                results['operationalStatus'] = macAddrDetail[i]['operationalStatus']
                results['deviceType'] = summary['deviceType']
                results['deviceName'] = summary['deviceName']
                results['ipAddress'] = summary['ipAddress']

    elif call == 'client' :
        print('client')
        device = response_json['queryResponse']['entity'][0]['clientDetailsDTO']
        results["macAddress"] = device['macAddress']
        results["ipAddress"] = device['ipAddress']
        results["connectionType"] = device['connectionType']
        results["clientInterface"] = device['clientInterface']
        results["deviceName"] = device['deviceName']
        results["deviceType"] = device['deviceType']
        results["deviceIpAddress"] = device['deviceIpAddress']

    elif call == 'device' :
        devices = response_json['queryResponse']['entity']
        records=[]
        for record in range(len(devices)) :
            device = devices[record]['inventoryDetailsDTO']
            summary = device['summary']
            udiDetail = device['udiDetails']['udiDetail']
            results = OrderedDict()
            results["deviceName"] = summary['deviceName']
            results["deviceType"] = summary['deviceType']
            results["ipAddress"] = summary['ipAddress']
            results["reachability"] = summary['reachability']
            module = 0

            if isinstance(udiDetail, list) :

                for i in range(len(udiDetail)):
                    devTest = udiDetail[i]
                    if (('productId' in devTest) and (searchValue in devTest['productId'])):
                        print('*****$$$ module is: ', module, '$$$****')
                        if (module == 0) :
                            results["productId"] = udiDetail[i]['productId']
                            results["name"] = udiDetail[i]['name']
                            results["udiSerialNr"] = udiDetail[i]['udiSerialNr']
                            module = module +1
                        else:
                            results["---- additional sub-modules ----"] = '------------------------'
                            results["productId" + str(module)] = udiDetail[i]['productId']
                            results["name" + str(module)] = udiDetail[i]['name']
                            results["udiSerialNr" + str(module)] = udiDetail[i]["udiSerialNr"]
                            print('results[productId + str(module)]', results["productId" + str(module)])
                            module = module +1

            elif isinstance(udiDetail, dict) :
                devTest = udiDetail
                if (('productId' in devTest) and (searchValue in devTest['productId'])):
                    print('*****$$$ module is: ', module, '$$$****')
                    if (module == 0):
                        results["productId"] = udiDetail['productId']
                        results["name"] = udiDetail['name']
                        results["udiSerialNr"] = udiDetail['udiSerialNr']
                        module = module + 1
                    else:
                        results["---- additional sub-modules ----"] = '------------------------'
                        results["productId" + str(module)] = udiDetail[i]['productId']
                        results["name" + str(module)] = udiDetail[i]['name']
                        results["udiSerialNr" + str(module)] = udiDetail[i]["udiSerialNr"]
                        print('results[productId + str(module)]', results["productId" + str(module)])
                        module = module + 1

            records.append(results)

        return (records)

    elif call == 'software' :
        devices = response_json['queryResponse']['entity']
        records=[]
        for record in range(len(devices)):
            device = devices[record]['devicesDTO']
            results = OrderedDict()
            results["deviceName"] = device['deviceName']
            results["deviceType"] = device['deviceType']
            results["ipAddress"] = device['ipAddress']
            results["softwareType"] = device['softwareType']
            results["softwareVersion"] = device['softwareVersion']
            records.append(results)
            print('records for itereation: ', record, 'is :\n', records)
        return (records)

    return (results)








