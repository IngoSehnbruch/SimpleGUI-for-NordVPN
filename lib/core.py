# This python script uses the following encoding: utf8
from ensurepip import version
import os
from tkinter import HIDDEN
import PySimpleGUI as sg
import webbrowser
from datetime import datetime
from time import sleep

from lib import core_vars as var
from lib import core_functions as cf
from lib import core_gui as gui
from lib import core_nordvpn as vpnControl


#* GLOBALS
window = None
vpnSettings = None
vpnStatus = None


#* ---------- GUI STYLE ----------

# sg.theme('DarkBlue1')  

sg.set_options(
        #icon                            = var.icon, 
        font                            = var.font, 

        button_color                    = var.buttonbgcolors,
        input_text_color                = var.textcolor,
        scrollbar_color                 = var.textcolor,
        text_color                      = var.textcolor,
        element_text_color              = var.textcolor,

        background_color                = var.windowbgcolor, 
        element_background_color        = var.windowbgcolor, 
        text_element_background_color   = var.windowbgcolor,
        input_elements_background_color = var.windowbgcolor,

        margins = (5,10),
        element_padding = (5, 2),
    )

sg.SetGlobalIcon( var.icon )


#* ---------- WINDOW STUFF ----------

def getWindowPosition():
    #global window
    pos = None
    try:
        if window:
            pos = window.CurrentLocation()
    except:
        pass

    if not pos and var.SETTINGS['remember_position']: 
        pos = var.SETTINGS['window_position']
        if pos == [None, None]: pos = None
    if not pos: pos = var.defaultwindowposition

    return pos


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
        with open(os.path.join(var.logfolder, str(datetime.now().strftime('%Y%m%d')) + "_log.txt"), "a") as logfile:
            logfile.write(logstr + "\n")
        #* simple error-logs:
        if error:
            with open(os.path.join(var.logfolder, str(datetime.now().strftime("%Y%m%d")) + "_errorlog.txt"), "a") as logfile:
                logfile.write(logstr + "\n")
            # add as csv to todos for upload to dashboard
            with open(os.path.join(var.logfolder, "errorlog.csv"), "a") as logfile:
                logfile.write(logstr.replace(' > ', var.separator) + "\n")

    #* write to screen
    if window: 
        wlog = window['-LOG-'].get() 
        if wlog: wlog += '\n\n' 
        window['-LOG-'].update(wlog + str(logstr) )
    window.Refresh()

    if var.SETTINGS['use_terminal']:
        print(logstr)
    

#* ------------------------------------------------------------------- HELPER TASKS

def setStatusToLoading():
    window['-btnConnect-'].update('LOADING...')
    window['-statusicon-'].update(filename=var.statusicon['grey'])
    window.Refresh()


def updateQuickset():
    window['-quick-keep on top-'].update(var.SETTINGS['keep_on_top'])
    window['-quick-notify-'].update( (vpnSettings['settings']['Notify']=='enabled') )
    window['-quick-autoconnect-'].update( (vpnSettings['settings']['Auto-connect']=='enabled') )
    window['-quick-killswitch-'].update( (vpnSettings['settings']['Kill Switch']=='enabled') )

def updateViewVisibiliy():
    # Reorder by turning out and depending on setting on again in desired order (otherwise it will be appended to the end)
    for v, vsetting in var.SETTINGS['view_visibility'].items():
        window['frame' + v].hide_row()
        if vsetting: window['frame' + v].unhide_row()
    window.Refresh()

def checkAccountStatus():
    global vpnSettings

    account = vpnControl.vpnLoadAccount()
    while not account.get('Email Address'):
        # ask to login
        todo = gui.getSingleChoice(wintitle="Please login to NordVPN", wintext=["You are not logged in.", "Please login to your NordVPN Account."], valuelist=['Login at NordVPN Website', 'Register at NordVPN Website', 'Exit NordVPN-GUI'], selectfirst=True)
        if todo == 'Login at NordVPN Website':
            reply = vpnControl.vpnLogin()
            try:
                url = (reply[0][0]).split(": ")[1]
                webbrowser.open(url, new=2)
                gui.showInfo("Confirm when logged in", ['Your Browser has opened the NordVPN Loginpage.', 'Please confirm once you are logged in.'])
                account = vpnControl.vpnLoadAccount() # if successful while ends
            except Exception as err:
                log(str(reply), str(err))
                break
        elif todo=="Register at NordVPN Website":
            url = var.LINKS['nordvpn']['register']
            webbrowser.open(url, new=2)
            gui.showInfo("Confirm when registered", ['Your Browser has opened the NordVPN Homepage.', 'Please confirm once you are logged in.'])
            account = vpnControl.vpnLoadAccount() # if successful while ends
            if not account.get('Email Address'):
                gui.showInfo("Confirm when logged in", ['Your Browser has opened the NordVPN Loginpage.', 'Please confirm once you are logged in.'])
                account = vpnControl.vpnLoadAccount() # if successful while ends
        else:
            quit()
    
    vpnSettings = vpnControl.vpnLoadSettings()
    return True


#* ------------------------------------------------------------------- ACTIONS


def updateStatus():
    global vpnStatus
    status = None

    #* GET VPN Status
    try:
        vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars
        status = vpnStatus['Status']
    except Exception as err:
        gui.showInfo('ERROR', ['NO VPN STATUS AVAILABLE.', "(" + str(err) + ")"])

    try:
        if status == "Connected":
            # Beautify utime-info
            if "second" in vpnStatus['Uptime'].split(' ')[1]:
                vpnStatus['Uptime'] = "Leass than a minute."
            else:
                if 'minutes' in vpnStatus['Uptime']:
                    vpnStatus['Uptime'] = vpnStatus['Uptime'].split('minutes')[0] + "mins"
                elif 'minute' in vpnStatus['Uptime']:
                    vpnStatus['Uptime'] = vpnStatus['Uptime'].split('minute')[0] + "min"        
            
            # UPDATE WINDOW
            window['-status-Uptime-'].update(vpnStatus['Uptime'])
            window['-status-Country-'].update(vpnStatus['Country'])
            window['-status-Server IP-'].update(vpnStatus['Server IP'])
            
            window['-btnConnect-'].update('DISCONNECT')
            window['-statusicon-'].update(filename=var.statusicon['green'])

            #window.iconbitmap(var.statusicon['green'])
            window.set_icon( var.statusicon['green'] )
        else:
            # UPDATE WINDOW
            window['-status-Uptime-'].update('NOT CONNECTED')
            window['-status-Country-'].update('NOT CONNECTED')
            window['-status-Server IP-'].update('NOT CONNECTED')
            
            window['-btnConnect-'].update('CONNECT')
            window['-statusicon-'].update(filename=var.statusicon['red'])
            #window.iconbitmap(var.statusicon['red'])
            window.set_icon( var.statusicon['red'] )

        window.Refresh()
    except Exception as err:
        log("Status-Update Error", str(err))

    return datetime.now()


def select_server(selection=None, country=None):
    global vpnSettings
    #window.Hide()

    reply = None
    selections = ['Automatic', 'by Country', 'by City', 'by Type']
    if var.SETTINGS['lastconnection'] is not None and var.SETTINGS['lastconnection'] != 'Automatic':
        selections = [ var.SETTINGS['lastconnection'] ] + selections

    if selection == None:
        selection = gui.getSingleChoice(wintitle="Select Server", wintext=["Select from what list to choose"], valuelist=selections, selectfirst=True)
    
    if selection == var.SETTINGS['lastconnection']:
        setStatusToLoading()
        reply = vpnControl.vpnConnect( var.SETTINGS['lastconnection'] )

    if selection == 'Automatic':
        setStatusToLoading()
        reply = vpnControl.vpnConnect('Automatic')

    if selection == 'by Country' or (selection == 'by City' and country==None):
        country = gui.getSingleChoice_Dropdown(wintitle="Select Server", wintext=["Select the country"], valuelist=vpnSettings['countries'], selectfirst=False)
        if selection == 'by Country' and country: 
            setStatusToLoading()
            reply = vpnControl.vpnConnect(country)
        
    if selection == 'by City' and country:
        city = country = gui.getSingleChoice_Dropdown(wintitle="Select Server", wintext=["Select the city:"], valuelist=vpnSettings['citydict'][country], selectfirst=False)
        if city: 
            setStatusToLoading()
            reply = vpnControl.vpnConnect(city)
    
    if selection == 'by Type':
        servertype = country = gui.getSingleChoice_Dropdown(wintitle="Select Server", wintext=["Select the servertype:"], valuelist=vpnSettings['vpngroups'], selectfirst=False)
        if servertype: 
            setStatusToLoading()
            reply = vpnControl.vpnConnect(servertype)
    
    if reply: log(reply[0])

    window.UnHide()
    window.Refresh()
    updateStatus()


#* ------------------------------------------------------------------- SETTINGS (and SPLASH)

def settings_gui():
    settingswindowtitle = 'GUI Settings'

    layout_cb_gui = [
                    [ sg.Checkbox('Keep Window on Top', default = var.SETTINGS['keep_on_top'], key='keep_on_top', enable_events=True, tooltip=' Allways show GUI on top of all windows '), ],
                    [ sg.Checkbox('Dark Mode', default = var.SETTINGS['darkmode'], key='darkmode', enable_events=True, tooltip=' Use dark colors '), ],
                    [ sg.Checkbox('Remember Windowposition', default = var.SETTINGS['remember_position'], key='remember_position', enable_events=True, tooltip=' Remember the Windowposition after restart'), ],
                ]
    layout_cb_log = [
                    [ sg.Checkbox('Log to terminal', default = var.SETTINGS['use_terminal'], key='use_terminal', enable_events=True, tooltip=' If false log-output will be send to terminal '), ],
                    [ sg.Checkbox('Log to file', default = var.SETTINGS['log'], key='log', enable_events=True, tooltip=' Log to file '), ],
                ]

    layout_cb_dev = [
                    [ sg.Checkbox('Debug Mode', default = var.SETTINGS['DEBUG'], key='DEBUG', enable_events=True, tooltip=' DEBUG MODE - FOR DEVELOPMENT '), ],
                ]

    layout_settings = [
        [ sg.Frame(" GUI ", layout_cb_gui, size=(300, 110)), ],
        [ sg.Frame(" LOG ", layout_cb_log, size=(300, 110)), ],
        [ sg.Frame(" DEV ", layout_cb_dev, size=(300, 60)), ],

        [ sg.Text('', font=('Segoe UI', 2) ) ],
        [   
            sg.Button('SAVE', size=(12,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(12,1), button_color=('white', var.colors['red'])),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    window_settings.BringToFront()
    window.Hide()

    # Window Event Loop
    while True:  
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                window_settings.close()
                window.UnHide()
                return False

            elif event == 'SAVE':
                window_settings.close()
                window.UnHide()
                window.Refresh()

                # apply changes
                for setting in values:
                    var.SETTINGS[setting] = values[setting]

                if var.SETTINGS['remember_position']:
                    try:
                        var.SETTINGS['window_position'] = window.CurrentLocation()
                    except:
                        var.SETTINGS['window_position'] = False
                else:
                    var.SETTINGS['window_position'] = False
                
                var.saveSettings()

                updateStatus()
                return True


def settings_vpn():
    global vpnSettings
    #refresh in case console was used to change settings
    vpnSettings = vpnControl.vpnLoadSettings()

    settingswindowtitle = 'VPN Settings'

    layout_cb_vpn = []
    for setvar in var.settingsDict.keys():
        if var.settingsDict[setvar][0] == 'boolean':
            setval = (vpnSettings['settings'][var.settingsDict[setvar][1]] == 'enabled')
            layout_cb_vpn.extend([
                    [ sg.Checkbox(var.settingsDict[setvar][1], default = setval, key="checkbox-"+setvar, enable_events=True, tooltip=var.settingsDict[setvar][2]), ],            
                ])

    layout_set_dns = [
        [ sg.Button('SET DNS', size=(12,1), ), sg.Text( vpnSettings['settings']['DNS'], key='SET_DNS' ), ],
    ]

    layout_set_technology = [
        [ sg.Button('SET TECH', size=(12,1), ), sg.Text(vpnSettings['settings']['Technology'], key='SET_TECHNOLOGY' ), ],
    ]


    layout_settings = [
        [ sg.Frame(" VPN ", layout_cb_vpn, size=(300, 230)), ],
        [ sg.Frame(" DNS ", layout_set_dns, size=(300, 65)), ],
        [ sg.Frame(" TECHNOLOGY ", layout_set_technology, size=(300, 65)), ],
        [ sg.Text('', font=('Segoe UI', 2) ) ],
        [   
            sg.Button('SAVE', size=(10,1), button_color=('white', 'darkgreen')),
            sg.Button('CANCEL', size=(10,1), button_color=('white', var.colors['red'])),
        ],   
    ]

    window_settings = sg.Window(settingswindowtitle, layout_settings, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered
    window_settings.BringToFront()
    window.Hide()

    while True:
        event, values = window_settings.read(timeout=0)
        if event != '__TIMEOUT__':

            if event == 'CANCEL' or event == 'EXIT' or event== sg.WIN_CLOSED:
                window_settings.close()
                window.UnHide()
                break

            elif event == 'SET DNS':
                newdns = gui.getValue(wintitle="DNS SERVERS", wintext=["SET DNS SERVERS:", "A list of max 3 IP addresses separated by space.", "Leave empty to disable. Example:", "0.0.0.0 1.2.3.4"], defaulttext=vpnSettings['settings']['DNS'])
                if newdns == "": newdns = "disabled"
                if newdns and newdns != vpnSettings['settings']['DNS']:
                    reply = vpnControl.vpnSet('dns', newdns)[0]
                    log(reply[0])
                    vpnSettings = vpnControl.vpnLoadSettings()
                    window_settings['SET_DNS'].update(vpnSettings['settings']['DNS'])
                    gui.showInfo("DNS", reply, )

            elif event == 'SET TECH':
                newtech = gui.getSingleChoice(wintitle="Please choose VPN Technology", wintext=["Supported values for [technology]:", "OpenVPN or NordLynx"] , valuelist= ['OpenVPN', 'NordLynx', ], selectfirst=False)
                if newtech and newtech != vpnSettings['settings']['Technology']:
                    reply = vpnControl.vpnSet('technology', newtech)[0]
                    log(reply[0])
                    vpnSettings = vpnControl.vpnLoadSettings()
                    window_settings['SET_TECHNOLOGY'].update(vpnSettings['settings']['Technology'])
                    gui.showInfo("Technology", reply, )

            elif event == 'SAVE':
                # apply changes
                changes = 0
                changelog = []
                for setvarname, setval in values.items():
                    if "checkbox-" in setvarname:
                        setvartitle = var.settingsDict[setvarname.replace("checkbox-", "")][1]
                        setvar = setvarname.replace("checkbox-", "")
                        
                        if setval: 
                            setvarto = "enabled" 
                        else:
                            setvarto = "disabled"

                        if vpnSettings['settings'][ setvartitle ] != setvarto:
                            changes += 1
                            reply = vpnControl.vpnSet(setvar, setvarto)[0]
                            log(reply[0])
                            changelog = changelog + reply

                window_settings.close()
                
                if changes == 0:
                    gui.showInfo(wintitle="Nothing changed", wintext=['No settings changed.',])
                else:
                    vpnSettings = vpnControl.vpnLoadSettings()
                    gui.showInfo(wintitle=str(changes) + ' CHANGES:', wintext=changelog )
                
                window.UnHide()
                updateStatus()
                break


def splashwindow():
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

    # INIT-POPUP-SPLASH
    layout = [
        [ sg.Image(filename=var.logo, expand_x=True, background_color=var.splashbgcolor)],
        [ sg.Text(windowtitle, font=('Segoe UI', 14), text_color=var.splastextcolor, background_color=var.splashbgcolor) ],
        [ sg.Text('[ AN UNOFFICIAL ADD-ON ]', font=('Segoe UI', 10), text_color=var.splastextcolor, background_color=var.splashbgcolor) ],
        [ sg.Text(background_color=var.splashbgcolor) ],
        [ sg.Text('VERSION ' + var.appversion, font=('Segoe UI', 10), text_color=var.splastextcolor, background_color=var.splashbgcolor) ],
        [ sg.Text(background_color=var.splashbgcolor, font=('Segoe UI', 6),) ],
    ]

    window = sg.Window('Loading ...', layout, location=getWindowPosition(), background_color=var.splashbgcolor, element_justification='center', alpha_channel = 1, keep_on_top=True, finalize=True) #.centered

    window.Refresh()
    vpnSettings = vpnControl.vpnLoadSettings()

    checkAccountStatus()

    vpnStatus = vpnControl.vpnStatus()[1] # ignore text, only grab vars
    window.close()
    window = None
    
    
#* ---------- MAIN WINDOW ----------------------------------------------------------------------------------------------------

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

    # ------ Menu Definition ------ #

    menu_def = [
                ['SimpleGUI', [ 
                    'GUI Settings', 
                    'Reset GUI Settings',
                    '---', 
                    'Restart', 
                    'Exit']
                ],
                ['NordVPN', [ 
                        'VPN Settings',
                        'Reset VPN Settings',
                        '---', 
                        'Connect', ['Automatic', 'by Country', 'by City', 'by Type'],
                        'Disconnect',
                        '---', 
                        'What is my IP?',
                        '---', 
                        'Account', [ 'Account Info', '---', 'Login', 'Logout', '---',  'Register', ], 
                    ]
                ],
                ['View', [ 
                    'Hide All', 
                    'Show All',
                    '---', 
                    'Toggle Status', 
                    'Toggle Quickset',
                    'Toggle Log',
                    '---',
                    'Toggle Colormode',
                    ]
                ],
                ['?', ['About', 'Help']],
            ]

    MENU_RIGHT_CLICK = ['', [ 
                    'Hide All', 
                    'Show All',
                    '---', 
                    'Toggle Status', 
                    'Toggle Quickset', 
                    'Toggle Log', 
                    '---',
                    'Toggle Colormode',
                    '---',
                    'GUI Settings',
                    'VPN Settings',
                    '---',
                    'Cancel',
                    ]]  
    
    # ------ Layout Elements ------ #

    statusicon = [
                    [ sg.Image(filename=var.statusicon['grey'], key='-statusicon-', expand_x=True)],
                ]

    mainbuttons = [
                    [ sg.Button('LOADING...', font=('Segoe UI', 18), size=(10,1), key='-btnConnect-'), ],
                    [ sg.Button('SELECT SERVER', size=(15,1), button_color=('white', var.colors['purple']), key='-btnSelectServer-' ), ],
                ]

    layout_status = [
                        [ sg.Text('Uptime:', size=(10,1) ), sg.Text('---', key='-status-Uptime-' ) ],
                        [ sg.Text('Country:', size=(10,1) ), sg.Text('---', key='-status-Country-' ) ],
                        [ sg.Text('Server IP:', size=(10,1) ), sg.Text('---', key='-status-Server IP-' ) ],
                    ]
    size_status = (300,115)

    layout_quickset = [
                        [   
                            sg.Checkbox('Keep on Top', default = var.SETTINGS['keep_on_top'], key='-quick-keep on top-', enable_events=True, tooltip=' Allways show this Windowon on top.'),
                            sg.Checkbox('Notifications', default = (vpnSettings['settings']['Notify']=='enabled'), key='-quick-notify-', enable_events=True, tooltip=' Show Notifications (in OS). '), 
                        ],
                        [   
                            sg.Checkbox('Autoconnect', default = (vpnSettings['settings']['Auto-connect']=='enabled'), key='-quick-autoconnect-', enable_events=True, tooltip=' Autoconnect to NordVPN on System-Startup.'), 
                            sg.Checkbox('Kill Switch', default = (vpnSettings['settings']['Kill Switch']=='enabled'), key='-quick-killswitch-', enable_events=True, tooltip=' Disable internetaccess if not connected to a vpn. '), 
                        ],
                    ]
    size_quickset = (300,90)

    layout_log = [
            [sg.Multiline(size=(50, 5), font=('Courier New', 8), text_color = var.log_text_color, background_color=var.log_background_color, tooltip='LOG', key='-LOG-', auto_refresh=True, autoscroll=True, )],
        ]
    size_log = (300,100)

    # LAYOUT - Putting it all together...

    layout = [
                [ sg.Menu(menu_def, tearoff=False, pad=(200, 1), background_color = var.menu_background_color, text_color = var.menu_text_color, disabled_text_color = var.menu_disabled_text_color, key='Menu') ],
                [ sg.Column(statusicon, element_justification='c'), sg.Column(mainbuttons, element_justification='c') ],
                [ sg.Frame(" STATUS ", layout_status, size=size_status, key='frameStatus', pad=5 ) ],
                [ sg.Frame(" QUICKSET ", layout_quickset, size=size_quickset, key='frameQuickset', pad=5 ) ],
                [ sg.Frame(" LOG ", layout_log, size=size_log, key='frameLog', pad=5 ), ],
    ]
       
    window = sg.Window(windowtitle, layout, location=getWindowPosition(), element_justification='center', alpha_channel = 1, keep_on_top=var.SETTINGS['keep_on_top'], right_click_menu=MENU_RIGHT_CLICK, finalize=True) #.use var.window_positionfixed
    
    #! needs a nice window...?
    if var.SETTINGS['DEBUG'] and vpnSettings.get('infos'): 
        for i in vpnSettings.get('infos'):
            log(i)
    
    updateViewVisibiliy()
    


def startApp():
    global window
    global vpnSettings
    global vpnStatus

    # init app
    splashwindow()
    mainwindow()
    updateViewVisibiliy()
    status_ts = updateStatus()

    # Main Window Event Loop
    # Wait for Command
    # Update Status every 60 seconds
    while True:  

        # EVERY 60 SECONDS:
        if (datetime.now() - status_ts).seconds > 60: 
            
            # UPDATE VPN STATUS
            status_ts = updateStatus() 

            # UPDATE WIN POS IF NEEDED
            if var.SETTINGS['remember_position'] and window.CurrentLocation() != var.SETTINGS['window_position']:
                var.SETTINGS['window_position']=window.CurrentLocation()
                var.saveSettings()


        # HANDLE USER-INPUT EVENTS

        event, values = window.read(timeout=0)
    
        if event != '__TIMEOUT__':
            reply = None

            if event == sg.WIN_CLOSED or event == 'EXIT' or event == 'Exit':
                try:
                    window.Close()
                except:
                    pass
                return True

            # UPDATE WIN POS IF NEEDED
            if var.SETTINGS['remember_position'] and window.CurrentLocation() != var.SETTINGS['window_position']:
                var.SETTINGS['window_position']=window.CurrentLocation()
                var.saveSettings()

            if event == 'Restart':
                window.Close()
                window = None
                return False

            elif event == '-btnConnect-':
                # connect / disconnect vpn
                if vpnStatus['Status'] == 'Connected':
                    window['-btnConnect-'].update('LOADING...')
                    window['-statusicon-'].update(filename=var.statusicon['grey'])
                    window.set_icon( var.statusicon['grey'] )
                    window.Refresh()
                    reply = vpnControl.vpnDisconnect()
                    sleep(5) # wait a bit to finish "network-recovery"
                else:
                    window['-btnConnect-'].update('LOADING...')
                    window['-statusicon-'].update(filename=var.statusicon['grey'])
                    window.set_icon( var.statusicon['grey'] )
                    window.Refresh()
                    reply = vpnControl.vpnConnect()

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
                    if values[event]:
                        setvarto = 'enabled'
                    else:
                        setvarto = 'disabled'

                    reply = vpnControl.vpnSet(setvar, setvarto)[0]

            elif event == "Show All":
                for v, vsetting in var.SETTINGS['view_visibility'].items():
                    var.SETTINGS['view_visibility'][v] = True
                var.saveSettings()
                updateViewVisibiliy()
            
            elif event == "Hide All":
                for v, vsetting in var.SETTINGS['view_visibility'].items():
                    var.SETTINGS['view_visibility'][v] = False
                var.saveSettings()
                updateViewVisibiliy()

            elif 'Toggle ' in event:
                
                view = event.replace('Toggle ', '')
                if view == 'Menu':
                    window['Menu'].hide_row() #! NOT WORKING....
                elif view == 'Colormode':
                    if var.SETTINGS['darkmode']:
                        var.SETTINGS['darkmode'] = False
                    else:
                        var.SETTINGS['darkmode'] = True
                    var.saveSettings()
                    updateQuickset()
                    window.Close()
                    window = None
                    cf.restartApp()                
                else:
                    if var.SETTINGS['view_visibility'][view]:
                        window['frame' + view].hide_row()
                        var.SETTINGS['view_visibility'][view] = False
                    else:
                        window['frame' + view].unhide_row()
                        var.SETTINGS['view_visibility'][view] = True
                
                var.saveSettings()
                updateViewVisibiliy()

            # ---- MENU ITEMS -----

            elif event == 'GUI Settings': 
                restart = settings_gui()
                if restart:
                    window.Close()
                    window = None
                    cf.restartApp()

            elif event == 'Reset GUI Settings': 
                if gui.getConfirmation('Reset GUI Settings?', ['Are you sure you want to reset the GUI Settings?', 'This will e restart the app.']):
                    if os.path.exists(var.settings_jsonfile): 
                        os.remove(var.settings_jsonfile) #? reset gui settings
                    window.Close()
                    window = None
                    cf.restartApp()

            elif event == 'VPN Settings': 
                settings_vpn()
                updateQuickset()

            elif event == 'Reset VPN Settings': 
                if gui.getConfirmation('Reset VPN Settings?', [
                    'Are you sure you want to reset your vpn settings to default?', 
                    'This will end an existing connection and restart the app.',
                    'You will be logged out from Nord VPN Account.',
                    ]):
                    log(vpnControl.vpnDisconnect()[0][0])
                    log(vpnControl.vpnResetSettings()[0][0])
                    window.Close()
                    window = None
                    cf.restartApp()
            
            elif event == 'Automatic':
                window['-btnConnect-'].update('LOADING...')
                window['-statusicon-'].update(filename=var.statusicon['grey'])
                window.set_icon( var.statusicon['grey'] )
                window.Refresh()
                reply = vpnControl.vpnConnect()

            elif 'by ' in event:
                #serverBy = event.replace('Server ', ''))
                reply = select_server(event)

            elif event == 'Disconnect':
                window['-btnConnect-'].update('LOADING...')
                window['-statusicon-'].update(filename=var.statusicon['grey'])
                window.set_icon( var.statusicon['grey'] )
                window.Refresh()
                reply = vpnControl.vpnDisconnect()
                sleep(5) # wait a bit to finish "network-recovery"

            elif event == "Login":
                vpnControl.vpnLogin()

            elif event == 'Logout':
                if gui.getConfirmation('Logout?', ['Are you sure you want to log out?', 'This will end any vpn connection and close the app.']):
                    reply = vpnControl.vpnLogout()
                    return True

            elif event == 'Account Info':
                infotext = [
                    'Account: '+ vpnSettings['account']['Email Address'],
                    'Service: '+ vpnSettings['account']['VPN Service']
                ]
                gui.showInfo(wintitle='NordVPN Account', wintext=infotext)

            elif event == 'What is my IP?':
                url = var.LINKS['nordvpn']['ip']
                webbrowser.open(url, new=2)

            elif event == 'Register':
                url = var.LINKS['nordvpn']['register']
                webbrowser.open(url, new=2)

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
                gui.showInfo(wintitle=event, wintext=infotext)
                
            elif event == 'Help':
                infotext = [
                        'This GUI is an inofficial frontend for the nordvpn terminal application.',
                        'You can download the terminal app at ' + var.LINKS['nordvpn']['install'],
                        '',
                        'For help about the gui visit ' + var.LINKS['gui']['github'],
                    ]
                gui.showInfo(wintitle=event, wintext=infotext)
            
            elif event == "Cancel":
                pass

            else:
                log("UNKNOWN COMMAND: " + str(event), str(values)) #* for dev & bugfixing (should not happen)

            if reply: log(reply[0])
            status_ts = updateStatus()