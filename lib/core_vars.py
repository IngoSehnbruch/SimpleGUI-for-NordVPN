# This python script uses the following encoding: utf8
import os
import sys

#* app defaults
appversion = "0.1"
icon = "pynordvpn.ico"
separator = ";"

SETTINGS = {
    'DEBUG' : True, # get a boolean value
    'autostart': False,
    'autoconnect': False,
    'console' : True,
    'logdetailed' : False,
    'keep_on_top' : True,
    'window_positionfixed' : False, # e.g. (750, 220) or false
}

LINKS = {
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


#* folders
appfolder = os.path.dirname(sys.argv[0])
logfolder = os.path.join(appfolder, 'logs')
datafolder = os.path.join(appfolder, 'data')

mediafolder = os.path.join(appfolder, 'media')
splash = os.path.join(mediafolder, 'logo_nordvpn.png')