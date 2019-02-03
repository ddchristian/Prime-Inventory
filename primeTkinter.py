from tkinter import *
from startup import check_startup
from queryMethods import getDevice



def get_entry_data():

    print("Query Selected:", query_gui.get())
    print("MAC Option is:", macVar.get())
    print("Device Option:", dtypeVar.get())
    print("Software Option:", stypeVar.get())
    print("Search Value:", searchValue_gui.get())
    query_options = {'macAddrQ' : macVar.get(), 'deviceTypeQ' : dtypeVar.get(), 'softwareQ' : stypeVar.get()}
    if query_gui.get() not in ['serialNumberQ', 'ipAddrQ']:
        option = query_options[query_gui.get()]
        if 'Network' in option:
            option = 'network'
        elif 'Client' in option:
            option = 'client'
    else:
        option = ''

    entries = {}
    entries["query"] = query_gui.get()
    entries["MAC Option is:"] = macVar.get()
    entries["Device Option:"] = dtypeVar.get()
    entries["Software Option:"] = stypeVar.get()
    entries["searchValue"] = searchValue_gui.get()
    entries["option"] = option
    for key, value in entries.items():
        print(key, value)
    display_options(entries)


def display_options():


    startup_vars = check_startup(spark_bot=False)
    print('From __main__: startup_vars=', startup_vars)
    print('new startup_vars =', startup_vars)

    query_options = {'macAddrQ' : macVar.get(), 'deviceTypeQ' : dtypeVar.get(), 'softwareQ' : stypeVar.get()}
    queryType = {'serialNumberQ': 'Serial Number', 'ipAddrQ': 'IP Address', 'macAddrQ': 'MAC Address',
                 'deviceTypeQ': 'Device Type', 'softwareQ': 'Software Type'}

    query = query_gui.get()
    searchValue = searchValue_gui.get()

    if query not in ['serialNumberQ', 'ipAddrQ']:
        option = query_options[query.get()]
        if 'Network' in option:
            option = 'network'
        elif 'Client' in option:
            option = 'client'
    else:
        option = ''


    '''
    Label(gui, text='').grid(row=22)
    Label(gui, text='').grid(row=23)
    Label(gui, text='').grid(row=24)
    Label(gui, text='Variable Selection:', font=("Arial", 18)).grid(row=25, column=0, sticky=W)

    start_row = 26
    for key, value in entries.items():
        print(start_row)
        print(key, value)
        Label(gui, text=key, width=15, borderwidth=2, relief=SUNKEN).grid(row=start_row, column=0, ipadx=30)
        Label(gui, text=value, width=15, borderwidth=2, relief=SUNKEN).grid(row=start_row, column=1, ipadx=30)
        start_row = start_row +1


    '''



    print('query is:', query)
    print('option is:', option)
    print('searchValue is:', searchValue)
    result = getDevice(startup_vars, query, searchValue, option)

    height = str(500 + (len(result))*20)
    print('height = ', height)

    gui.geometry('550x' + height)

    Label(gui, text='').grid(row=22)
    Label(gui, text='').grid(row=23)

    if query in ['serialNumberQ', 'ipAddrQ', 'macAddrQ']:
        print('\n\nSummary details for search with', queryType[query], ':', searchValue, '!')
        query_text = 'Summary details for search with ' + queryType[query] + ': ' + searchValue + '!'
        print(('query_text = ', query_text))
        Label(gui, text = query_text, font=("Arial", 18)).grid(row=24, column=0, sticky=W)
        Label(gui, text = '').grid(row=25)

        for key, value in result.items():
            print(key, ' : ', value)

        start_row = 26
        for key, value in result.items():
            print(start_row)
            print(key, value)
            Label(gui, text=key, width=15, borderwidth=2, relief=SUNKEN).grid(row=start_row, column=0, sticky=E)
            Label(gui, text=value, width=45, borderwidth=2, relief=SUNKEN).grid(row=start_row, column=1, sticky=W)
            start_row = start_row +1

    if query in ['softwareQ', 'deviceTypeQ']:
        print('Total records found: ', len(result), '\n\n')
        for record in range(len(result)):
            print('Record Number: ', record + 1)
            print('----------------------------------------\n')
            for key, value in result[record].items():
                print(key, ':', value)
            print('\n\n')
    if not result: print('Nothing returned from search. Item', searchValue, 'not found in Prime database.')


def reset_options():
    query_gui.set("serialQ")
    macVar.set("Network Mac")
    dtypeVar.set("Equal")
    stypeVar.set("IOS-XE")
    searchValue_gui.delete(0, 'end')



gui = Tk()

gui.geometry('550x500')

rows = 0
while rows < 80:
    gui.rowconfigure(rows, weight=1)
    gui.columnconfigure(rows, weight=1)
    rows += 1



gui.title('Prime Infrastructure Quick Search Tool')

Label(gui, text='Select Query Type', font=("Arial Bold", 20)).grid(row=0, sticky=W)

query_gui = StringVar()
query_gui.set("serialNumberQ") # initialize to value = 1
Radiobutton(gui, text='Serial Number', variable=query_gui, value="serialNumberQ").grid(row=1, column=0, sticky=W)
Radiobutton(gui, text='IP Address', variable=query_gui, value='ipAddrQ').grid(row=2, column=0, sticky=W)
Radiobutton(gui, text='MAC Address', variable=query_gui, value='macAddrQ').grid(row=3, sticky=W)
macVar = StringVar(gui)
macVar.set("Network Mac") # default value
macOption = OptionMenu(gui, macVar, "Network Mac", "Client Mac")
macOption.grid(row=3,column=1, sticky=W)

Radiobutton(gui, text='Device Type', variable=query_gui, value='deviceTypeQ').grid(row=4, sticky=W)
dtypeVar = StringVar(gui)
dtypeVar.set("Equal") # default value
deviceOption = OptionMenu(gui, dtypeVar, "Equal", "Contains")
deviceOption.grid(row=4,column=1, sticky=W)

Label(gui, text='Search Value:').grid(row=12, sticky=W)
searchValue_gui = Entry(gui)
searchValue_gui.grid(row=13, sticky=W)

Radiobutton(gui, text='Software Type', variable=query_gui, value='softwareQ').grid(row=16, sticky=W)
stypeVar = StringVar(gui)
stypeVar.set("IOS-XE") # default value
softwareOption = OptionMenu(gui, stypeVar, "IOS-XE", "IOS", "NX-OS", "Controller")
softwareOption.grid(row=16,column=1, sticky=W)

submit = Button(gui, text='Submit', font=("Arial", 16), width=10, height=2, command=display_options)
reset = Button(gui, text='Reset', font=("Arial", 16), width=10, height=2, command=reset_options)
exit_gui = Button(gui, text='Exit', font=("Arial", 16), width=10, height=2, command=gui.destroy)

submit.grid(row=20, column=0)
reset.grid(row=20, column=1)
exit_gui.grid(row=20, column=2)

gui.mainloop()
