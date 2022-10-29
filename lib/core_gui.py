# This python script uses the following encoding: utf8
import os
import PySimpleGUI as sg

import json

from datetime import datetime
from time import sleep

from lib import core_vars as var
from lib import core_nordvpn as vpnControl

#* GLOBALS
window = None
vpnSettings = None
vpnStatus = None

#* ---------- GUI STYLE ----------

sg.theme('DarkBlue1')  # please make your windows colorful : ) #DarkGrey14
sg.set_options(icon = var.icon, font=('Segoe UI', 12) )

#* ---------- LOGGING ----------

def log(title, text="", error=False):
    logstr = ""
    if error:
        logstr += str(title) + " > ERROR > " + str(text)
    else:
        if title:
            logstr +=  str(title)
        if text:
            if title:
                logstr += " > "
            logstr += str(text)

    logstr = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " > " + logstr.upper()

    #* write to file:
    if var.SETTINGS['log']:
        with open(os.path.join(var.logfolder, "log_processing.txt"), "a") as logfile:
            logfile.write(logstr + "\n")
        #* simple error-logs:
        if error:
            with open(os.path.join(var.logfolder, str(datetime.now().strftime("%Y%m%d")) + "_errorlog.txt"), "a") as logfile:
                logfile.write(logstr + "\n")
            # add as csv to todos for upload to dashboard
            with open(os.path.join(var.logfolder, "errorlog.csv"), "a") as logfile:
                logfile.write(logstr.replace(' > ', var.separator) + "\n")

    #* write to screen
    print(logstr)
    window.Refresh()


#* ---------- GUI STUFF ----------

def getWindowPosition():
    #global window
    pos = None
    try:
        if window:
            pos = window.CurrentLocation()
    except:
        pass
    
    if not pos:
        if var.SETTINGS['remember_position']:
            pos = var.SETTINGS['window_position']
        else:
            pos = var.defaultwindowposition

    return pos


    print('POS', pos)
    return pos


def processWindow(wintitle="Processing...", wintext=['Process is running. Please wait.',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
        
    return sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    


def showInfo(wintitle="Info", wintext=['Information',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1))])
    
    window.Hide()
    infowindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, values = infowindow.read()
    infowindow.close()
    window.UnHide()

    if event == 'OK':
        return True
    else:
        return True # there is no false here ...

def getConfirmation(wintitle="Confirm", wintext=['Please confirm',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))])
    
    window.Hide()
    confirmationwindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, values = confirmationwindow.read()
    confirmationwindow.close()
    window.UnHide()

    if event == 'OK':
        return True
    else:
        return False

def getMultipleChoice(wintitle="Please choose", wintext="Min 1 choice:", valuelist= ['none',], selectall=False):
    layout = [[sg.Text(wintext + ':')],]
    for vitem in valuelist:
        layout.append([sg.Checkbox(vitem, default=selectall)])
    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))])
    
    window.Hide()
    choicewindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, choices = choicewindow.read()
    choicewindow.close()
    window.UnHide()

    if event == 'OK':
        if choices:
            newlist = []
            i=-1
            for option in valuelist:
                i+=1
                if choices[i]:
                    newlist.append(valuelist[i])
            return newlist
        else:
            showInfo('Aborted', ["Nothing seected"])
            return False
    else:
        return False

def getSingleChoice(wintitle="Please choose", wintext="1 choice:", valuelist= ['none',], selectfirst=False):
    layout = [[sg.Text(wintext)],]
    i=0
    for vitem in valuelist:
        i+=1
        if i==1 and selectfirst:
            layout.append([sg.Radio(vitem, 0, True)])
        else:
            layout.append([sg.Radio(vitem, 0)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))])
    
    window.Hide()
    choicewindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, choices = choicewindow.read()
    choicewindow.close()
    window.UnHide()

    if event == 'OK':
        newlist = []
        choice = None
        if choices:
            i=-1
            for option in valuelist:
                i+=1
                if choices[i]:
                    choice = valuelist[i]
            if choice:
                return choice
            else:
                return False
        else:
            showInfo('Aborted', ["Nothing seected"])
            return False
    else:
        return False



def getSingleChoice_Dropdown(wintitle="Please choose", wintext="1 choice:", valuelist= ['none',], selectfirst=False):
    layout = [[sg.Text(wintext + ':')],]
    
    layout.append([ sg.InputCombo(( valuelist ), font=('Courier New', 12), key='-choice-'),                ])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))])
    
    window.Hide()
    choicewindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, values = choicewindow.read()
    choicewindow.close()
    window.UnHide()

    if event == 'OK':
        newlist = []
        if values['-choice-'] in valuelist:
            return values['-choice-']
        else:
            showInfo('Aborted', ["Nothing seected"])
            return False
    else:
        return False


def getFile(wintitle="File", wintext="Choose a file", filetypes=("all", "*.*")):
    layout = [[sg.Text(wintext + ':')],
                [sg.Input(size=(40,1), visible=True), sg.FileBrowse(button_text='FILES', size=(10, 1), file_types=(filetypes,))],
                [sg.Text('')],
                [sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))] ]
    
    window.Hide()
    filewindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, files = filewindow.read()
    filewindow.close()
    window.UnHide()

    if event == 'OK':
        if files[0]:
            return files[0]
        else:
            showInfo('No File', ["No file selected"])
            return False
    else:
        return False

def getValue(wintitle="Value", wintext="Please ender value", defaulttext=''):
    layout = [[sg.Text(wintext + ':')],
                [sg.Input(size=(40,1), default_text = defaulttext)],
                [sg.Text('')],
                [sg.OK(button_text='OK', size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', 'darkred'), size=(23, 1))] ]
    
    window.Hide()
    valuewindow = sg.Window(wintitle, layout, location=getWindowPosition(), keep_on_top=True)
    event, values = valuewindow.read()
    
    valuewindow.close()
    window.UnHide()

    if event == 'OK':
        if values[0]:
            return values[0]
        else:
            showInfo('Info', ["Kein Value angegeben"])
            return False
    else:
        return False


#* -------------------------------------------------------------------

def updateStatus():
    global vpnStatus
    status = None
    skipGuiUpdate = [ 'Status', ]
    try:
        vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars
        status = vpnStatus['Status']
    except Exception as err:
        showInfo('ERROR', ['NO VPN STATUS AVAILABLE.', "(" + str(err) + ")"])

    if status == "Connected":

        window['-btnConnect-'].update('DISCONNECT', button_color = ('white','darkgreen'))
        window['-status-Country-'].update(vpnStatus['Country'])
        window['-status-Server IP-'].update(vpnStatus['Server IP'])
        window['-status-Current technology-'].update(vpnStatus['Current technology'])
        window['-status-Current protocol-'].update(vpnStatus['Current protocol'])
        

        if 'minutes' in vpnStatus['Uptime']:
            vpnStatus['Uptime'] = vpnStatus['Uptime'].split('minutes')[0] + "mins"
        elif 'minute' in vpnStatus['Uptime']:
            vpnStatus['Uptime'] = vpnStatus['Uptime'].split('minute')[0] + "min"
        
        window['-status-Uptime-'].update(vpnStatus['Uptime'])
    else:
        window['-btnConnect-'].update('CONNECT', button_color = ('white','darkred'))
        window['-status-Country-'].update('NOT CONNECTED')
        window['-status-Server IP-'].update('NOT CONNECTED')
        window['-status-Current technology-'].update('NOT CONNECTED')
        window['-status-Current protocol-'].update('NOT CONNECTED')
        window['-status-Uptime-'].update('NOT CONNECTED')

    window.Refresh()
    return datetime.now()


def select_server(selection=None, country=None):
    global vpnSettings
    window.Hide()

    reply = None

    selections = ['Automatic', 'by Country', 'by City', 'by Type']
    if selection == None:
        selection = getSingleChoice(wintitle="Select Server", wintext="Select from what list to choose:", valuelist=selections, selectfirst=True)
    
    if selection == 'Automatic':
        reply = vpnControl.vpnConnect('Automatic')

    if selection == 'by Country' or (selection == 'by City' and country==None):
        country = getSingleChoice_Dropdown(wintitle="Select Server", wintext="Select the country:", valuelist=vpnSettings['countries'], selectfirst=False)
        if selection == 'by Country' and country: reply = vpnControl.vpnConnect(country)
        
    if selection == 'by City' and country:
        city = country = getSingleChoice_Dropdown(wintitle="Select Server", wintext="Select the city:", valuelist=vpnSettings['citydict'][country], selectfirst=False)
        if city: reply = vpnControl.vpnConnect(city)
    
    if selection == 'by Type':
        servertype = country = getSingleChoice_Dropdown(wintitle="Select Server", wintext="Select the servertype:", valuelist=vpnSettings['vpngroups'], selectfirst=False)
        if servertype: reply = vpnControl.vpnConnect(servertype)
    
    if reply: log(reply[0])
    
    window.UnHide()
    updateStatus()


def settings_gui():
    
    # theme_name_list = sg.theme_list()

    settingswindowtitle = 'GUI Settings'

    layout_cb_gui = [
                    [ sg.Checkbox('Keep Window on Top', default = var.SETTINGS['keep_on_top'], key='keep_on_top', enable_events=True, tooltip=' Allways show GUI on top of all windows '), ],
                    [ sg.Checkbox('Remember Windowposition', default = var.SETTINGS['remember_position'], key='remember_position', enable_events=True, tooltip=' Remember the Windowposition after restart'), ],
                    [ sg.Checkbox('Log to file', default = var.SETTINGS['log'], key='log', enable_events=True, tooltip=' Log to file '), ],
                    [ sg.Checkbox('Show console', default = var.SETTINGS['console'], key='console', enable_events=True, tooltip=' If false log-output will be send to terminal '), ],
                ]

    layout_settings = [
        [ sg.Frame(" GUI ", layout_cb_gui, size=(300, 150)), ],
        [ sg.Text('', font=('Segoe UI', 2) ) ],
        [   
            sg.Button('SAVE', size=(12,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(12,1), button_color=('white', 'darkred')),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    window_settings.BringToFront()
    window.Hide()
    while True:  # Event Loop
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':
            #! SAVE LAST WINDOW POSITION!?
            # print(window_settings.CurrentLocation())

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                #basics.bot2api("info", "OFFLINE")
                #print('SETTINGS WINDOW POSITION:', window_settings.CurrentLocation())
                window_settings.close()
                window.UnHide()
                break
            elif event == 'SAVE':
                                
                #! apply changes
                for setting in values:
                    var.SETTINGS[setting] = values[setting]

                if var.SETTINGS['remember_position']:
                    var.SETTINGS['window_position'] = window.CurrentPosition()
                else:
                    var.SETTINGS['window_position'] = False
                
                var.saveSettings()
                
                window_settings.close()
                window.UnHide()
                updateStatus()
                break


def settings_vpn():
    global vpnSettings
    #refresh in case console was used to change settings
    vpnSettings = vpnControl.vpnLoadSettings()

    settingswindowtitle = 'VPN Settings'

    #print(vpnSettings['settings'])

    layout_cb_vpn = []
    for setvar in var.settingsDict.keys():
        if var.settingsDict[setvar][0] == 'boolean':
            setval = (vpnSettings['settings'][var.settingsDict[setvar][1]] == 'enabled')
            layout_cb_vpn.extend([
                    [ sg.Checkbox(var.settingsDict[setvar][1], default = setval, key="checkbox-"+setvar, enable_events=True, tooltip=var.settingsDict[setvar][2]), ],            
                ])

    layout_settings = [
        [ sg.Frame(" VPN ", layout_cb_vpn, size=(300, 250)), ],
        
        [ sg.Text('', font=('Segoe UI', 2) ) ],

        [   
            sg.Button('SAVE', size=(12,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(12,1), button_color=('white', 'darkred')),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    window_settings.BringToFront()
    window.Hide()

    while True:  # Event Loop
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':
            #! SAVE LAST WINDOW POSITION!?
            # print(window_settings.CurrentLocation())

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                #basics.bot2api("info", "OFFLINE")
                #print('SETTINGS WINDOW POSITION:', window_settings.CurrentLocation())
                window_settings.close()
                window.UnHide()
                break
            elif event == 'SAVE':
                #print(event, values)
                                
                # apply changes
                changes = 0
                changelog = []
                for setvarname, setval in values.items():
                    if "checkbox-" in setvarname:
                        setvartitle = var.settingsDict[setvarname.replace("checkbox-", "")][1]
                        setvar = setvarname.replace("checkbox-", "")
                        
                        setvarto = "disabled"
                        if setval: setvarto = "enabled"
                        #print(var.settingsDict[setvar.replace("checkbox-", "")][1])
                        #print( vpnSettings['settings'][ var.settingsDict[setvar.replace("checkbox-", "")][1] ])
                        if vpnSettings['settings'][ setvartitle ] != setvarto:
                            changes += 1
                            #print('nordvpn', 'set', setvar, setvarto)
                            reply = vpnControl.vpnSet(setvar, setvarto)[0]
                            log(reply[0])
                            changelog = changelog + reply

                window_settings.close()
                window.UnHide()

                if changes == 0:
                    showInfo(wintitle="Nothing changed", wintext=['No settings changed.',])
                else:
                    vpnSettings = vpnControl.vpnLoadSettings()
                    showInfo(wintitle=str(changes) + ' CHANGES:', wintext=changelog )
                
                updateStatus()
                break



#* ---------- MAIN GUI ----------------------------------------------------------------------------------------------------

def mainwindow():
    global window
    global vpnSettings
    global vpnStatus

    if window:
        try:
            window.Close()
        except:
            pass
        window = None

    windowtitle = 'SimpleGUI for NordVPN'
    areaVisibility = { 'Status' : True, 'Quickset' : True }

    #! INIT-POPUP-SPLASH
    layout = [
        [ sg.Image(filename=var.splash, expand_x=True)],
        [ sg.Text(windowtitle, font=('Segoe UI', 14)) ],
        [ sg.Text('[AN UNOFFICIAL ADD-ON]', font=('Segoe UI', 10)) ],
        [ sg.Text() ],
    ]

    #if not var.SETTINGS['window_position']:
    #    window = sg.Window('Loading ...', layout, element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    #else:
    window = sg.Window('Loading ...', layout, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered

    window.Refresh()
    vpnSettings = vpnControl.vpnLoadSettings()
    vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars
    window.close()
    window = None
    
    #! needs a nice window...
    #if vpnSettings.get('infos'):
    #    showInfo(wintitle="NordVPN Infos", wintext=vpnSettings.get('infos'))

    #print(vpnSettings)

    #! MAIN WINDOW

    # ------ Menu Definition ------ #
    menu_def = [
                ['SimpleGUI', [ 'GUI Settings', '---', 'Restart', 'Exit']],
                ['NordVPN', [ 
                        'VPN Settings', 
                        '---', 
                        'Connect', ['Automatic', 'by Country', 'by City', 'by Type'],
                        'Disconnect',
                        'Update Status',
                        '---', 
                        'Account', [ 'Login', 'Logout', '---', 'Account Info', 'Register', ], 
                    ]
                ],

                ['?', ['About', 'Help']],
            ]

    MENU_RIGHT_CLICK = ['', [ 'Toggle Status', 'Toggle Quickset', ]]  #'Toggle Console'
    
    layout_status = [
                        #[ sg.Text('Account:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('...', font=('Segoe UI', 10), key='-status-Account-' ) ],       
                        #[ sg.Text('VPN Status:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('...', font=('Segoe UI', 10), key='-status-Status-' ) ],    
                        #[ sg.Text('', font=('Segoe UI', 2) ) ],
                        [ sg.Text('Uptime:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Uptime-' ) ],
                        #[ sg.Text('', font=('Segoe UI', 2) ) ],
                        [ sg.Text('Country:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Country-' ) ],
                        [ sg.Text('Server IP:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Server IP-' ) ],
                        [ sg.Text('Technology:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Current technology-' ) ],
                        [ sg.Text('Protocol:', font=('Segoe UI', 10), size=(12,1) ), sg.Text('---', font=('Segoe UI', 10), key='-status-Current protocol-' ) ],
                    ]
    size_status = (300,165)
    #if vpnStatus['Status'] == "disconnected": size_status = (300,100)

    layout_quickset = [
                        [   
                            sg.Checkbox('Keep on Top', default = var.SETTINGS['keep_on_top'], key='-quick-keep on top-', enable_events=True, tooltip=' Allways show this Windowon on top.'),
                            sg.Checkbox('Kill Switch', default = (vpnSettings['settings']['Kill Switch']=='enabled'), key='-quick-killswitch-', enable_events=True, tooltip=' Disable internetaccess if not connected to a vpn. '), 
                        ],
                    ]
    size_quickset = (300,60)

    menu_text_color = '#ffffff'
    menu_disabled_text_color = '#999999'
    menu_background_color = '#3d3d3d'

    layout = [
                [sg.Menu(menu_def, tearoff=False, pad=(200, 1), background_color = menu_background_color, text_color = menu_text_color, disabled_text_color = menu_disabled_text_color, key='Menu')],
                #[ sg.Text( 'User: ' + vpnSettings['account']['Email Address'], font=('Segoe UI', 8) ) ],
                #[ sg.Text( vpnSettings['account']['VPN Service'] , font=('Segoe UI', 8) ) ],
                [ sg.Text('', font=('Segoe UI', 2) ) ],
                [   
                    sg.Button('Loading...', button_color=('grey', 'darkgrey'), font=('Segoe UI', 18), size=(19,1), key='-btnConnect-'),
                ],
                [   
                    sg.Button('SELECT SERVER', size=(28,1), key='-btnSelectServer-'),
                ],
                [ sg.Text('', font=('Segoe UI', 2) ) ],
                [ sg.Frame(" STATUS ", layout_status, size=size_status, key='frameStatus' ), ],
                [ sg.Frame(" QUICKSET ", layout_quickset, size=size_quickset, key='frameQuickset' ), ],
    ]

    # CONSOLE
    if var.SETTINGS['console']:
        layout_console = [
                [sg.Output(size=(50, 5), font=('Courier New', 8), text_color = '#d3d3d3', background_color='#000000', tooltip='LOG', key='-OUTPUT-')],
            ]
        size_console = (300,100)
        layout.extend([
            [ sg.Frame(" LOG ", layout_console, size=size_console, key='frameConsole' ), ],        
        ])

    layout.extend([[ sg.Text('', font=('Segoe UI', 2), key='lastLine' ) ], ])
        

    # create window
    #if not var.SETTINGS['window_position']:
    #    window = sg.Window(windowtitle, layout, element_justification='center', alpha_channel = 1, keep_on_top=var.SETTINGS['keep_on_top'], right_click_menu=MENU_RIGHT_CLICK, finalize=True) #.centered
    #else:
    window = sg.Window('SimpleGUI for NordVPN', layout, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=var.SETTINGS['keep_on_top'], right_click_menu=MENU_RIGHT_CLICK, finalize=True) #.use var.window_positionfixed
    window.Refresh()

    status_ts = updateStatus()

    while True:  # Event Loop

        # EVERY 60 SECONDS:
        if (datetime.now() - status_ts).seconds > 60: 
            
            # UPDATE VPN STATUS
            status_ts = updateStatus() 

            # UPDATE WIN POS IF NEEDED
            if var.SETTINGS['remember_position'] and window.CurrentLocation() != var.SETTINGS['window_position']:
                #print(window.CurrentLocation())
                var.SETTINGS['window_position']=window.CurrentLocation()
                var.saveSettings()


        # HANDLE USER-INPUT EVENTS

        event, values = window.read(timeout=0)

        if event != '__TIMEOUT__':
            reply = None
            #! SAVE LAST WINDOW POSITION!
            
            if event == sg.WIN_CLOSED or event == 'EXIT' or event == 'Exit':
                window.Close()
                return True

            elif event == 'Restart':
                window.Close()
                window = None
                return False

            elif event == '-btnConnect-':
                # connect / disconnect vpn
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

            elif event == '-btnSelectServer-':
                select_server()

            elif '-quick-' in event:

                if event == '-quick-keep on top-':
                    if values['-quick-keep on top-']:
                        window.keep_on_top_set()
                    else:
                        window.keep_on_top_clear()
                else:
                    # QUICKSET A VPN SETTING
                    setvar = event.replace('-quick-','')[:-1]
                    #print(values[event])
                    if values[event]:
                        setvarto = 'enabled'
                    else:
                        setvarto = 'disabled'

                    #print('nordvpn', 'set', setvar, setvarto)
                    reply = vpnControl.vpnSet(setvar, setvarto)[0]

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
                        #print(k, v)
                        if v:
                            window['lastLine'].unhide_row()
                            break


            # ---- MENU ITEMS -----

            elif event == 'GUI Settings': 
                settings_gui()


            elif event == 'VPN Settings': 
                settings_vpn()
            
            elif event == 'Automatic':
                window['-btnConnect-'].update('CONNECTING...', button_color = ('white','darkgrey'))
                window.Refresh()
                reply = vpnControl.vpnConnect()

            elif 'by ' in event:
                #serverBy = event.replace('Server ', ''))
                reply = select_server(event)

            elif event == 'Disconnect':
                window['-btnConnect-'].update('DISCONNECTING...', button_color = ('white','darkgrey'))
                window.Refresh()
                reply = vpnControl.vpnDisconnect()
                sleep(5) # wait a bit to finish "network-recovery"

            elif event == 'Update Status':
                #  updateStatus() ends after this
                pass

            elif event == 'Logout':
                if getConfirmation('Logout?', ['Are you sure you want to log out?', 'This will end any vpn connection and close the app.']):
                    reply = vpnControl.vpnLogout()
                    if os.path.exists(var.settings_jsonfile): os.remove(var.settings_jsonfile) #? reset gui settings
                    return True

            elif event == 'Account Info':
                infotext = [
                    'Account: '+ vpnSettings['account']['Email Address'],
                    'Service: '+ vpnSettings['account']['VPN Service']
                ]
                showInfo(wintitle='NordVPN Account', wintext=infotext)


            elif event == 'About':
                infotext = [
                        '[inofficial] SimpleGUI for NordVPN - Version ' + var.appversion,
                        'Installed terminal app: ' + vpnSettings['vpnversion'],
                        '',
                        'This GUI is an inofficial frontend for the nordvpn terminal application.',
                        'You can download the terminal app at ' + var.LINKS['nordvpn']['install'],
                        '',
                        'Homepage for the GUI: ' + var.LINKS['gui']['github'],
                        '',
                        'This project is open source. You can use this gui as you please.'
                    ]
                showInfo(wintitle=event, wintext=infotext)
                
            elif event == 'Help':
                infotext = [
                        'This GUI is an inofficial frontend for the nordvpn terminal application.',
                        'You can download the terminal app at ' + var.LINKS['nordvpn']['install'],
                        '',
                        'For help about the gui visit ' + var.LINKS['gui']['github'],
                    ]
                showInfo(wintitle=event, wintext=infotext)


            else:
                print(event, values) #* for dev & bugfixing (should not happen)

            if reply: log(reply[0])
            status_ts = updateStatus()            

        # LOOP ^

    #* EXIT
