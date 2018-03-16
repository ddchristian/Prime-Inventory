from startup import check_startup
from queryMethods import getDevice

startup_vars = check_startup(spark_bot=False)
print('From __main__: startup_vars=', startup_vars)
print('new startup_vars =', startup_vars)

query_options = {'A' : 'serialNumberQ',  'B' : 'ipAddrQ', 'C' : 'macAddrQ', 'D' : 'deviceTypeQ', 'E' : 'softwareQ'}
mac_options = {'A' : 'network',  'B' : 'client'}
searchOp_options = {'A' : 'eq',  'B' : 'startsWith', 'C' : 'contains'}
software_options = {'A' : 'IOS',  'B' : 'IOS-XE', 'C' : 'NX-OS', 'D' : 'Cisco Controller'}
queryType = {'serialNumberQ': 'Serial Number', 'ipAddrQ': 'IP Address', 'macAddrQ': 'MAC Address', 'deviceTypeQ': 'Device Type', 'softwareQ': 'Software Type'}

print('\nA Serial Number \nB IP Address \nC MAC Address \nD Device Type \nE Software Version')
query = input('Select the query type(A, B, C, etc.): ')
query = query_options[query.upper()]

option = ''
if query == 'macAddrQ':
    mac = input('Select the MAC lookup type(A or B):\nA Network MAC \nB Client MAC')
    option = mac_options[mac.upper()]
elif query == 'deviceTypeQ':
    searchOp = input('Select the search option for Device Type (A, B or C):\nA Equal \nB Starts With \nC Contains')
    option = searchOp_options[searchOp.upper()]
elif query == 'softwareQ' :
    print('\nA IOS \nB IOS-XE \nC NX-OS \nD Cisco Controller')
    software = input('Select the software type (A, B or C):')
    option = software_options[software.upper()]
    searchValue =''

if not query == 'softwareQ' :
    searchValue = input('\nEnter search value:\n').upper().strip()

print('query is:', query)
print('option is:', option)
print('searchValue is:', searchValue)
result = getDevice(startup_vars, query, searchValue, option)

if query in ['serialNumberQ', 'ipAddrQ', 'macAddrQ'] :
    print('\n\nSummary details for search with', queryType[query], ':', searchValue, '!')
    for key, value in result.items() :
        print(key, ' : ', value)



if query in ['softwareQ', 'deviceTypeQ'] :
    print('Total records found: ', len(result), '\n\n')
    for record in range(len(result)) :
        print('Record Number: ', record + 1)
        print('----------------------------------------\n')
        for key, value in result[record].items() :
            print(key, ':', value)
        print('\n\n')
if not result : print('Nothing returned from search. Item', searchValue, 'not found in Prime database.')
