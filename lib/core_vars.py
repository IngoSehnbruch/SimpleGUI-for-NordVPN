# This python script uses the following encoding: utf8
import os
import sys
import json

#* app defaults
appversion = "0.1"
icon = "nordvpngui.ico"
separator = ";"


#* folders
appfolder = os.path.dirname(sys.argv[0])
logfolder = os.path.join(appfolder, 'logs')
#datafolder = os.path.join(appfolder, 'data')

mediafolder = os.path.join(appfolder, 'media')
splash = os.path.join(mediafolder, 'logo_nordvpn.png')

settings_jsonfile = os.path.join(appfolder, 'settings.json')

defaultwindowposition = (50, 50)

SETTINGS = {
    'DEBUG' : True, # get a boolean value
    'console' : True,
    'log' : False,
    'keep_on_top' : True,
    'remember_position' : False,
    'window_position' : False, # e.g. (750, 220) or false
    'lastconnection' : 'Automatic', # None = automatic
}

if os.path.exists(settings_jsonfile):
    with open(settings_jsonfile, 'r') as f:
        SETTINGS.update(json.load(f))


def saveSettings():
    with open(settings_jsonfile, 'w') as f:
        json.dump(SETTINGS, f, indent=4)


LINKS = {
    'gui' : { 
        'github' : 'https://github.com/IngoSehnbruch/SimpleGUI-for-NordVPN',
    },
    'nordvpn' : { 
        'install' : 'https://nordvpn.com/de/download/linux/',
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
    # defaults => Restores settings to their default values.

