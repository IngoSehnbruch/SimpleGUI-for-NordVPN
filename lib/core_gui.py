# This python script uses the following encoding: utf8
import os
import PySimpleGUI as sg
from datetime import datetime
from time import sleep

from lib import core_vars as var
from lib import core_nordvpn as vpnControl

#* GLOBALS
window = None
vpnSettings = None
vpnStatus = None
vpnServerNr = None

#* ---------- GUI STYLE ----------

sg.theme('DarkBlue1')  # please make your windows colorful : ) #DarkGrey14
sg.set_options(icon = var.icon, font=('Segoe UI', 12) )

#* ---------- LOGGING ----------

def log(title, text="", error=False):
    logstr = ""
    if error:
        logstr += title + " > ERROR > " + text
    else:
        if title:
            logstr +=  title
        if text:
            if title:
                logstr += " > "
            logstr += text

    logstr = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " > " + logstr.upper()

    #* write to file:
    with open(os.path.join(var.logfolder, "log_processing.txt"), "a") as logfile:
        logfile.write(logstr + "\n")
    #* simple error-logs:
    if error:
        with open(os.path.join(var.logfolder, str(datetime.now().strftime("%Y%m%d")) + "_errorlog.txt"), "a") as logfile:
            logfile.write(logstr + "\n")
        # add as csv to todos for upload to dashboard
        with open(os.path.join(var.logfolder, "errorlog.csv"), "a") as logfile:
            logfile.write(logstr.replace(' > ', var.separator) + "\n")

        #bot2api("error", None, "title="+urllib.parse.quote(title)+"&text="+urllib.parse.quote(text)+"&")
        # logfile.write("API CONNECTION FAILED" + "\n")

    #* write to screen
    print(logstr)
    window.Refresh()


#* ---------- GUI STUFF ----------

def processWindow(wintitle="Info", wintext=['Information',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
        
    return sg.Window(wintitle, layout, keep_on_top=True)
    


def showInfo(wintitle="Info", wintext=['Information',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1))])
    
    infowindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, values = infowindow.read()
    infowindow.close()

    if event == 'OK':
        return True
    else:
        return True # there is no false here ...

def getConfirmation(wintitle="Bestätigung", wintext=['Bitte bestätigen',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='WEITER', size=(22, 1)), sg.Cancel(button_text='ABBRECHEN', button_color=('white', 'darkred'), size=(23, 1))])
    
    confirmationwindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, values = confirmationwindow.read()
    confirmationwindow.close()

    if event == 'WEITER':
        return True
    else:
        return False

def getMultipleChoice(wintitle="Bitte wählen", wintext="Mindestens 1 Auswahl:", valuelist= ['none',], selectall=False):
    layout = [[sg.Text(wintext + ':')],]
    for vitem in valuelist:
        layout.append([sg.Checkbox(vitem, default=selectall)])
    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='WEITER', size=(22, 1)), sg.Cancel(button_text='ABBRECHEN', button_color=('white', 'darkred'), size=(23, 1))])
    
    choicewindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, choices = choicewindow.read()
    choicewindow.close()

    if event == 'WEITER':
        if choices:
            newlist = []
            i=-1
            for option in valuelist:
                i+=1
                if choices[i]:
                    newlist.append(valuelist[i])
            return newlist
        else:
            showInfo('Info', ["Nichts ausgewählt"])
            return False
    else:
        return False

def getSingleChoice(wintitle="Bitte wählen", wintext="1 Auswahl:", valuelist= ['none',], selectfirst=False):
    layout = [[sg.Text(wintext + ':')],]
    i=0
    for vitem in valuelist:
        i+=1
        if i==1 and selectfirst:
            layout.append([sg.Radio(vitem, 1)])
        else:
            layout.append([sg.Radio(vitem, 0)])
    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='WEITER', size=(22, 1)), sg.Cancel(button_text='ABBRECHEN', button_color=('white', 'darkred'), size=(23, 1))])
    
    choicewindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, choices = choicewindow.read()
    choicewindow.close()

    if event == 'WEITER':
        newlist = []
        if choices:
            i=-1
            for option in valuelist:
                i+=1
                if choices[i]:
                    choice = valuelist[i]
            return choice
        else:
            showInfo('Info', ["Nichts ausgewählt"])
            return False
    else:
        return False

def getFile(wintitle="Datei wählen", wintext="Wählen Sie eine Import-Datei", filetypes=("Alle Dateien", "*.*")):
    layout = [[sg.Text(wintext + ':')],
                [sg.Input(size=(40,1), visible=True), sg.FileBrowse(button_text='DATEIEN', size=(10, 1), file_types=(filetypes,))],
                [sg.Text('')],
                [sg.OK(button_text='WEITER', size=(22, 1)), sg.Cancel(button_text='ABBRECHEN', button_color=('white', 'darkred'), size=(23, 1))] ]
    filewindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, files = filewindow.read()
    filewindow.close()

    if event == 'WEITER':
        if files[0]:
            return files[0]
        else:
            showInfo('Info', ["Keine Datei ausgewählt"])
            return False
    else:
        return False

def getValue(wintitle="Wert Eintragen", wintext="Wert", defaulttext=''):
    layout = [[sg.Text(wintext + ':')],
                [sg.Input(size=(40,1), default_text = defaulttext)],
                [sg.Text('')],
                [sg.OK(button_text='WEITER', size=(22, 1)), sg.Cancel(button_text='ABBRECHEN', button_color=('white', 'darkred'), size=(23, 1))] ]
    valuewindow = sg.Window(wintitle, layout, keep_on_top=True)
    event, values = valuewindow.read()
    valuewindow.close()

    if event == 'WEITER':
        if values[0]:
            return values[0]
        else:
            showInfo('Info', ["Kein Wert angegeben"])
            return False
    else:
        return False


#* -------------------------------------------------------------------

def vpnOptions_setCountry():
    pass

def vpnOptions_setServer():
    pass

def updateStatus():
    global vpnStatus
    status = None
    try:
        vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars

        for statusvar, statusval in vpnStatus.items():
            if statusvar == "Uptime": 
                if 'minutes' in statusval:
                    statusval = statusval.split('minutes')[0] + "minutes"
                elif 'minute' in statusval:
                    statusval = statusval.split('minute')[0] + "minute"

            window['-status-' + statusvar + '-'].update(statusval)
        
        status = vpnStatus['Status']

    except Exception as err:
        showInfo('ERROR', ['NO VPN STATUS AVAILABLE.', "(" + str(err) + ")"])

    if status == "Connected":
        window['-btnConnect-'].update('DISCONNECT', button_color = ('white','darkgreen'))
    else:
        window['-btnConnect-'].update('CONNECT', button_color = ('white','darkred'))
        window['-status-Country-'].update('---')
        window['-status-Server IP-'].update('---')
        window['-status-Current technology-'].update('---')
        window['-status-Current protocol-'].update('---')
        window['-status-Uptime-'].update('---')

    window.Refresh()
    return datetime.now()


def settings_gui():

    # theme_name_list = sg.theme_list()

    settingswindowtitle = 'GUI Settings'

    layout_cb_gui = [
                    [ sg.Checkbox('Keep Window on Top', default = var.SETTINGS['keep_on_top'], key='-keep_on_top-', enable_events=True, tooltip=' Allways show GUI on top of all windows '), ],            
                    [ sg.Checkbox('Log connectionstatus', default = var.SETTINGS['logdetailed'], key='-detailedLog-', enable_events=True, tooltip=' Log to file '), ],
                ]

    layout_settings = [
        [ sg.Frame(" GUI ", layout_cb_gui, size=(300, 100)), ],
        [ sg.Text('', font=('Segoe UI', 2) ) ],
        [   
            sg.Button('SAVE', size=(12,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(12,1), button_color=('white', 'darkred')),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    while True:  # Event Loop
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':
            #! SAVE LAST WINDOW POSITION!?
            # print(window_settings.CurrentLocation())

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                #basics.bot2api("info", "OFFLINE")
                #print('SETTINGS WINDOW POSITION:', window_settings.CurrentLocation())
                window_settings.close()
                break
            elif event == 'SAVE':
                print(event, values)
                window_settings.close()
                
                #! apply changes

                updateStatus()
                break


def settings_vpn():
    global vpnSettings

    settingswindowtitle = 'VPN Settings'

    layout_cb_vpn = []
    for setvar in var.settingsDict.keys():
        if var.settingsDict[setvar][0] == 'boolean':
            setval = (vpnSettings['settings'][var.settingsDict[setvar][1]] == 'enabled')
            layout_cb_vpn.extend([
                    [ sg.Checkbox(var.settingsDict[setvar][1], default = setval, key='-'+setvar+'-', enable_events=True, tooltip=var.settingsDict[setvar][2]), ],            
                ])

    layout_settings = [
        [ sg.Frame(" VPN ", layout_cb_vpn, size=(300, 250)), ],
        
        [ sg.Text('', font=('Segoe UI', 2) ) ],

        [   
            sg.Button('SAVE', size=(12,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(12,1), button_color=('white', 'darkred')),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    while True:  # Event Loop
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':
            #! SAVE LAST WINDOW POSITION!?
            # print(window_settings.CurrentLocation())

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                #basics.bot2api("info", "OFFLINE")
                print('SETTINGS WINDOW POSITION:', window_settings.CurrentLocation())
                window_settings.close()
                break
            elif event == 'SAVE':
                print(event, values)
                window_settings.close()
                
                #! apply changes

                updateStatus()
                break



#* ---------- MAIN GUI ----------------------------------------------------------------------------------------------------

def mainwindow():
    global window
    global vpnSettings
    global vpnStatus

    windowtitle = 'SimpleGUI for NordVPN'
    areaVisibility = { 'Status' : True, 'Quickset' : True }

    #! INIT-POPUP-SPLASH
    layout = [
        [ sg.Image(filename=var.splash, expand_x=True)],
        [ sg.Text(windowtitle, font=('Segoe UI', 14)) ],
        [ sg.Text('[AN UNOFFICIAL ADD-ON by IS]', font=('Segoe UI', 10)) ],
        [ sg.Text() ],
    ]

    window = sg.Window('Loading ...', layout, element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    window.Refresh()
    vpnSettings = vpnControl.vpnLoadSettings()
    vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars
    # print (vpnSettings)
    window.close()


    #! MAIN WINDOW

    # ------ Menu Definition ------ #
    menu_def = [
                ['SimpleGUI', [ 'GUI Settings', '---', 'Restart', 'Exit']],
                ['NordVPN', [ 
                        'VPN Settings', 
                        '---', 
                        'Select Server', ['Automatic', 'by Country', 'by City', 'by Type'], 
                        'Connection', ['Connect', 'Disconnect', 'Update Status'],
                        '---', 
                        'Account', [ 'Info', '---', 'Login', 'Logout', 'Register', ], 
                    ]
                ],

                ['?', ['About', 'Help']],
            ]

    menu_background_color = '#d3d3d3'
    menu_text_color = '#000000'
    menu_disabled_text_color = '#999999'

    MENU_RIGHT_CLICK = ['', [ 'Toggle Status', 'Toggle Quickset', ]]   #! 'Toggle Menu',
    
    layout_status = [
                        [ sg.Text('Account:', font=('Segoe UI', 10), size=(12,1) ), sg.Text(vpnSettings['account']['Email Address'], font=('Segoe UI', 10) ) ],       
                        [ sg.Text('VPN Status:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('checking ...', font=('Segoe UI', 10), key='-status-Status-' ) ],    
                        [ sg.Text('', font=('Segoe UI', 2) ) ],
                        [ sg.Text('Country:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Country-' ) ],
                        [ sg.Text('Server IP:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Server IP-' ) ],
                        [ sg.Text('Technology:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Current technology-' ) ],
                        [ sg.Text('Protocol:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Current protocol-' ) ],
                        [ sg.Text('', font=('Segoe UI', 2) ) ],
                        [ sg.Text('Uptime:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Uptime-' ) ],
                    ]
    size_status = (300,250)
    #if vpnStatus['Status'] == "disconnected": size_status = (300,100)

    layout_quickset = [
                        [   
                            sg.Checkbox('Keep on Top', default = var.SETTINGS['keep_on_top'], key='-quick-keep on top-', enable_events=True, tooltip=' Allways show this Windowon on top.'),
                            sg.Checkbox('Kill Switch', default = (vpnSettings['settings']['Kill Switch']=='enabled'), key='-quick-killswitch-', enable_events=True, tooltip=' Disable internetaccess if not connected to a vpn. '), 
                        ],
                    ]
    size_quickset = (300,60)




    layout = [
                [sg.Menu(menu_def, tearoff=False, pad=(200, 1), background_color = menu_background_color, text_color = menu_text_color, disabled_text_color = menu_disabled_text_color, key='Menu')],
                #[ sg.Text( 'User: ' + vpnSettings['account']['Email Address'], font=('Segoe UI', 8) ) ],
                #[ sg.Text( vpnSettings['account']['VPN Service'] , font=('Segoe UI', 8) ) ],
                [ sg.Text('', font=('Segoe UI', 2) ) ],
                [   
                    sg.Button('SELECT SERVER', size=(28,1)),
                ],
                [   
                    sg.Button('Loading...', button_color=('grey', 'darkgrey'), font=('Segoe UI', 18), size=(19,1), key='-btnConnect-'),
                ],
                [ sg.Text('', font=('Segoe UI', 2) ) ],
                [ sg.Frame(" STATUS ", layout_status, size=size_status, key='frameStatus' ), ],
                [ sg.Frame(" QUICKSET ", layout_quickset, size=size_quickset, key='frameQuickset' ), ],
                [ sg.Text('', font=('Segoe UI', 2), key='lastLine' ) ],
    ]

        

    # create window
    if not var.SETTINGS['window_positionfixed']:
        window = sg.Window(windowtitle, layout, element_justification='center', alpha_channel = 1, keep_on_top=var.SETTINGS['keep_on_top'], right_click_menu=MENU_RIGHT_CLICK, finalize=True) #.centered
    else:
        window = sg.Window('SimpleGUI for NordVPN', layout, location=var.SETTINGS['window_positionfixed'], alpha_channel = 1, keep_on_top=var.SETTINGS['keep_on_top'], right_click_menu=MENU_RIGHT_CLICK, finalize=True) #.use var.window_positionfixed
    window.Refresh()

    status_ts = updateStatus()

    while True:  # Event Loop

        if (datetime.now() - status_ts).seconds > 60: status_ts = updateStatus()

        event, values = window.read(timeout=0)
        # eventhadling
        if event != '__TIMEOUT__':
            reply = []
            #! SAVE LAST WINDOW POSITION!
            # print(window.CurrentLocation())

            if event == 'EXIT' or event == sg.WIN_CLOSED: break

            if event == 'VPN Settings': 
                settings_vpn()

            elif event == '-btnConnect-':

                if vpnStatus['Status'] == 'Connected':
                    window['-btnConnect-'].update('DISCONNECTING...', button_color = ('white','darkgrey'))
                    window.Refresh()
                    reply = vpnControl.vpnDisconnect()
                    sleep(5) # wait a bit to finish "network-recovery"
                else:
                    window['-btnConnect-'].update('CONNECTING...', button_color = ('white','darkgrey'))
                    window.Refresh()
                    reply = vpnControl.vpnConnect()
                    #if "You are connected to" in reply[1]:
                    #    ServerNr = reply[1].split("#")[1].split(" ")[0]
                    #    window['-status-Country-'].update(ServerNr)

            elif '-quick-' in event:
                if event == '-quick-keep on top-':
                    if values['-quick-keep on top-']:
                        window.keep_on_top_set()
                    else:
                        window.keep_on_top_clear()
                else:
                    # QUICKSET A VPN SETTING
                    setvar = event.replace('-quick-','')[:-1]
                    print(values[event])
                    if values[event]:
                        setvarto = 'enabled'
                    else:
                        setvarto = 'disabled'

                    print('nordvpn', 'set', setvar, setvarto)
                    reply = vpnControl.vpnSet(setvar, setvarto)
                    print(reply)
            elif 'Toggle ' in event:
                
                area = event.replace('Toggle ', '')
                if area == 'Menu':
                    window['Menu'].hide_row() #! NOT WORKING....
                else:
                    window['lastLine'].hide_row()
                    if areaVisibility[area]:
                        window['frame' + area].hide_row()
                        areaVisibility[area] = False
                    else:
                        window['frame' + area].unhide_row()
                        areaVisibility[area] = True
                    for k, v in areaVisibility.items():
                        print(k, v)
                        if v:
                            window['lastLine'].unhide_row()
                            break

                print(window['frame' + area])
                #.unhide_row

            else:
                print(event, values) #* for dev & bugfixing (should not happen)

                print()

            #if len(reply)>0: print(reply)

            status_ts = updateStatus()

        # LOOP ^

    #* EXIT
