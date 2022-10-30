# This python script uses the following encoding: utf8
import sys

from lib import core_vars as var
from lib import core_functions as cf
from lib import core as core

#* ----- ----- INIT APP ----- ----- 



if __name__ == '__main__':

    if not cf.checkpath(var.logfolder): quit()
    if not cf.checkpath(var.datafolder): quit()    
    
    optionals = ['-terminal', '-log', '-reset']
    for arg in sys.argv[1:]:
        if arg=="-terminal" :   var.SETTINGS['use_terminal'] = True
        elif arg=="-log" :      var.SETTINGS['log'] = True
        elif arg=="-reset" :    var.settings_reset()
        else: 
            print("UNKNOWN ARGUMENT:", arg)
            quit()

    #* load GUI to continue
    end = False
    while not end:
        end = core.startApp()
