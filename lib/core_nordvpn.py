# This python script uses the following encoding: utf8
import os
from datetime import datetime
from time import sleep

from lib import core_vars as var
from lib.core_functions import runCommand, loadJsonFile, saveJsonFile

# varnames for nordvpn
vpnapp          = 'nordvpn'
settings_vars   = ['Technology' ,'Firewall', 'Kill Switch', 'Threat Protection Lite', 'Notify', 'Auto-connect', 'IPv6', 'Meshnet', 'DNS']
status_vars     = ['Status', 'Country', 'Server IP', 'Current technology', 'Current protocol', 'Uptime', ]

# ignore console-lines containing these strings (case sensitive)
lines_ignored   = ['A new version', 'New feature']

# Cache-Duration for vpn-details: available Countries, Cities and Groups. 0 for never use cache. Runs on Startup.
maxDaysCached   = 2 

def vpnConnect(server=None):
    # update "last connection"-info for quickconnec
    if not server and var.SETTINGS['lastconnection'] is not None: server = var.SETTINGS['lastconnection']

    if var.SETTINGS['lastconnection'] != server:
        var.SETTINGS['lastconnection'] = server # None = Automatic
        var.saveSettings()

    if not server or server == 'Automatic':
        reply = runCommand( [vpnapp, 'connect'], lines_ignored=lines_ignored )
    else:
        reply = runCommand( [vpnapp, 'connect', server], lines_ignored=lines_ignored )

    return reply

def vpnDisconnect():
    return runCommand( [vpnapp, 'disconnect'], lines_ignored=lines_ignored )

def vpnStatus():
    return runCommand( [vpnapp, 'status'] , varList=status_vars, lines_ignored=lines_ignored )

def vpnSet(setvar, setvarto):
    return runCommand( [vpnapp, 'set', setvar, setvarto] , varList=status_vars, lines_ignored=lines_ignored )

def vpnLogin():
    return runCommand( [vpnapp, 'login'] , varList=status_vars, lines_ignored=lines_ignored )

def vpnLogout():
    return runCommand( [vpnapp, 'logout'] , varList=status_vars, lines_ignored=lines_ignored )

def vpnRegister():
    return runCommand( [vpnapp, 'register'] , varList=status_vars, lines_ignored=lines_ignored )


def vpnLoadAccount():
    return runCommand( [vpnapp, 'account'], ['Email Address', 'VPN Service'], lines_ignored=lines_ignored )[1]

def vpnResetSettings():
    return runCommand( [vpnapp, 'set', 'defaults'], lines_ignored=lines_ignored )

def vpnLoadSettings():
    jsonVpnFile = os.path.join( var.datafolder, 'options_nordvpn.json')

    # GET NORD-VPN APP-VERSION (step by step - may not be installed!)
    vpnversion = "NOT INSTALLED"
    cmdreply = runCommand([vpnapp, 'version'], lines_ignored=lines_ignored)
    if not cmdreply:
        print("")
        print("ERROR: NordVPN dependencies not fount.")
        print("")
        print("Please install the NordVPN commandline application")
        print("from:", var.links[vpnapp]['install'])
        print("")
        sleep(3)
        quit()
    else:
        for line in cmdreply:
            if "Version" in line: vpnversion = line

    # CHECK FOR VALID CACHED JSONDATA    
    refreshJsonFile = True
    if maxDaysCached > 0 and os.path.exists(jsonVpnFile):
        jsondata = loadJsonFile(jsonVpnFile)
        jsondays = (datetime.now() - datetime.strptime(jsondata['timestamp'], "%Y-%m-%d %H:%M:%S")).days
        
        if jsondays <= maxDaysCached and jsondata['vpnversion'] == vpnversion:
            countries = jsondata['countries']
            citydict  = jsondata['citydict']
            vpngroups = jsondata['vpngroups']
            refreshJsonFile = False
        
        jsondata = None
        
    # LOAD APP-OPIONS IF NEEDED
    if refreshJsonFile:

        # GET COUNTRIES
        countries = []
        for line in runCommand([vpnapp, 'countries'], lines_ignored=lines_ignored):
            for section in line.split('\t'):

                # example line: Country Name 1       Country Name 2
                # split by more than one space and remove empty sections of variable length
                for sec in section.split('  '):
                    if len(sec)>1: countries.append(sec.strip())
        
        # REORDER
        countries.sort()

        # GET CITIES FOR EACH COUNTRY
        citydict = {}
        for country in countries:
            citylist = []
            for line in runCommand([vpnapp, 'cities', country], lines_ignored=lines_ignored):
                for section in line.split('\t'):
                    if len(section)>1: citylist.append(section)

            
            citylist.sort()
            citydict[country] = citylist

        # GET VGPNGROUPS
        vpngroups = []
        for line in runCommand([vpnapp, 'groups'], lines_ignored=lines_ignored):
            for section in line.split('\t'):
                if len(section)>1: vpngroups.append(section)
        vpngroups.sort()

        # cache to file
        saveJsonFile(jsonVpnFile, { 'timestamp': str(datetime.now()).split('.')[0], 'vpnversion' : vpnversion, 'countries' : countries, 'citydict': citydict, 'vpngroups' : vpngroups })

    # GET LOCAL SETTINGS (GET "lines_ignored" as "infos")
    infos, settings = runCommand( [vpnapp, 'settings'], varList=settings_vars )

    # GET ACCOUNT INFOS
    account = vpnLoadAccount()

    return {'vpnversion' : vpnversion, 'infos' : infos, 'countries' : countries, 'citydict': citydict, 'vpngroups' : vpngroups, 'settings' : settings, 'account' : account}
    