# This python script uses the following encoding: utf8
import os
import sys
import json

#* app defaults
appversion = "0.1"
icon = "nordvpngui.ico"
separator = ";"

minclientversion = "3.13.2"

#* folders
appfolder = os.path.dirname(sys.argv[0])
logfolder = os.path.join(appfolder, 'logs')
datafolder = os.path.join(appfolder, 'data')

mediafolder = os.path.join(appfolder, 'media')
splash = os.path.join(mediafolder, 'logo_nordvpn.png')
statusicon = {
        'green' : os.path.join(mediafolder, 'status_green_100.png'),
        'red' : os.path.join(mediafolder, 'status_red_100.png'),
        'grey' : os.path.join(mediafolder, 'status_grey_100.png'),
    }

settings_jsonfile = os.path.join(datafolder, 'settings.json')

defaultwindowposition = (50, 50)
font = ('Segoe UI', 12)



SETTINGS = {
    'DEBUG' : True, # get a boolean value
    'use_terminal' : False,
    'log' : False,
    'keep_on_top' : True,
    'remember_position' : True,
    'window_position' : defaultwindowposition, # e.g. (750, 220) or false
    'lastconnection' : 'Automatic', # None = automatic
    'darkmode' : False,

    'view_visibility' : { 'Status' : True, 'Quickset' : True, 'Log' : True, }
}

if os.path.exists(settings_jsonfile):
    with open(settings_jsonfile, 'r') as f:
        SETTINGS.update(json.load(f))


def saveSettings():
    with open(settings_jsonfile, 'w') as f:
        json.dump(SETTINGS, f, indent=4)



#! CI COLORS from NordVPN-brandbook

colors = {
    'blue' :        '#4687ff',
    'dark_blue' :   '#0e1b33',
    'red' :         "#F64F64",
    'orange' :      '#FF7E23',
    'purple' :      '#7F7AEE',
    'green' :       '#27BE56',

    'black' :       '#000000',
    'white' :       '#ffffff',
    'grey' :        '#999999',
    'dark_grey' :   '#333333',
    'light_grey' :  '#dddddd',
}

if SETTINGS['darkmode']:
    splashbgcolor = colors['dark_blue']
    splastextcolor = colors['white']

    windowbgcolor = colors['dark_blue']
    buttonbgcolors = (colors['white'], colors['blue'])
    connectbgcolor = colors['purple']
    textcolor = colors['white']

    menu_text_color = colors['white']
    menu_disabled_text_color = colors['grey']
    menu_background_color = colors['dark_grey']
else:
    splashbgcolor = colors['dark_blue']
    splastextcolor = colors['white']
    
    windowbgcolor = colors['white']
    buttonbgcolors = (colors['white'], colors['blue'])
    connectbgcolor = colors['purple']
    textcolor = colors['dark_blue']

    menu_text_color = colors['black']
    menu_disabled_text_color = colors['grey']
    menu_background_color = colors['light_grey']

LINKS = {
    'gui' : { 
        'homepage'  : 'https://github.com/IngoSehnbruch/SimpleGUI-for-NordVPN',
        'github'    : 'https://github.com/IngoSehnbruch/SimpleGUI-for-NordVPN',
    },
    'nordvpn' : { 
        'homepage'  : 'https://nordvpn.com/',
        'install'   : 'https://nordvpn.com/de/download/linux/',
        'register'  : 'https://nordvpn.com/pricing/'
    },
}

settingsDict = {
    'autoconnect' :             [ 'boolean', 'Auto-connect', ' Enables or disables auto-connect. \n When enabled, this feature will automatically \n try to connect to VPN on operating system startup. ' ],
    'killswitch' :              [ 'boolean', 'Kill Switch', ' Enables or disables Kill Switch. \n This security feature blocks your device from \n accessing the Internet while not connected to the VPN \n or in case connection with a VPN server is lost. ' ],
    'firewall' :                [ 'boolean', 'Firewall', ' Enables or disables use of the firewall. ' ],
    'tplite' :                  [ 'boolean', 'Threat Protection Lite', ' Enables or disables ThreatProtectionLite. \n When enabled, the ThreatProtectionLite feature will automatically \n block suspicious websites so that no malware or other cyber threats \n  can infect your device. Additionally, no flashy ads will come into your sight. \n More information on how it works: https://nordvpn.com/features/threat-protection/. ' ],
    'ipv6' :                    [ 'boolean', 'IPv6', ' Enables or disables use of the ipv6. ' ],
    'mesh' :                    [ 'boolean', 'Meshnet', ' Enables or disables meshnet on this device. ' ],
    'notify' :                  [ 'boolean', 'Notify', ' Enables or disables notifications ' ],

    'dns' :                     [ 'string', 'DNS', 'Set custom DNS servers. (Note: Setting DNS disables ThreatProtectionLite.)' ], # defaut: false
    'technology' :              [ 'select', 'Technology', 'Sets the technology', ['OpenVPN', 'NordLynx'] ],
}
