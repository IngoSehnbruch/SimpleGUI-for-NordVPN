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
            print('Path created: ' + pathname)
        return True
    except Exception as err:
        print("ERROR: PATH CAN NOT BE CREATED")
        print("PATH: " + pathname)
        print(err)
        return False

#* ----- ----- MAIN START ----- ----- 

if __name__ == '__main__':

    if not checkpath(var.logfolder): quit()
#    if not checkpath(var.datafolder): quit()

    autostart = False
    console = True
    logdetailed = False
    
    optionals = ['-terminal', '-log']
    for arg in sys.argv[1:]:
        if arg=="-terminal":    var.SETTINGS['console']     = False
        elif arg=="-log":       var.SETTINGS['log'] = True
        else: print("UNKNOWN ARGUMENT:", arg)

    #* load GUI to continue
    end = False
    while not end:        
        end = gui.mainwindow()

