# This python script uses the following encoding: utf8
import os
import sys

from lib import core_vars as var
from lib import core_gui as gui

#* ---------- PATHs

def checkpath(pathname):
    try:
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
            #print('Path created: ' + pathname)
        return True
    except Exception as err:
        print("ERROR: PATH CAN NOT BE CREATED")
        print("PATH: " + pathname)
        print(err)
        return False

#* ----- ----- MAIN START ----- ----- 

if __name__ == '__main__':

    if not checkpath(var.logfolder): quit()
    if not checkpath(var.datafolder): quit()

    autostart = False
    console = True
    logdetailed = False
    
    optionals = ['-autostart', '-terminal', '-logdetailed']
    for arg in sys.argv[1:]:
        if arg=="-autostart":       var.SETTINGS['autostart']   = True
        elif arg=="-terminal":      var.SETTINGS['console']     = False
        elif arg=="-logdetailed":   var.SETTINGS['logdetailed'] = True
        else: print("UNKNOWN ARGUMENT:", arg)

    #* Override autoconnect if autostart is true:
    if var.SETTINGS['autostart']: var.SETTINGS['autoconnect'] = True

    #* load GUI to continue
    gui.mainwindow()
