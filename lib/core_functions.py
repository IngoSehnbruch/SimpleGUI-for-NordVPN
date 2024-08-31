# This python script uses the following encoding: utf8
import subprocess
import os
import sys
import json


#* Check for PATHs
def checkpath(pathname):
    try:
        if not os.path.isdir(pathname):
            # os.makedir(pathname)
            os.makedirs(pathname)
            print('Path created: ' + pathname)
        return True
    except Exception as err:
        print("ERROR: PATH CAN NOT BE CREATED")
        print("PATH: " + pathname)
        print(err)
        return False


# run a consolecommand and return output as line (and optional generate a dict by given var-names)
def runCommand(cmd, varList=[], lines_ignored=[], donotskip = False):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
    
        textlines = [ ]
        varDict = { }
        for line in result.stdout.decode('utf-8').splitlines():
            # Filter Out "loadingwheel"
            if len(line)>3:
                # Add to var Dict or textlines
                if line.split(': ')[0] in varList:
                    varDict[line.split(': ')[0]] = line.split(': ')[1]
                else:
                    skip = False
                    for l in lines_ignored:
                        if l in line: skip = True
                    if not skip or donotskip: textlines.append(line)

    except Exception as err:
        #print("ERROR:", err)
        if varList != []:
            return False, False
        else:
            return False
    
    if varList != []:
        return textlines, varDict
    else:
        return textlines


# "hard" restart
def restartApp():
    os.execl(sys.executable, sys.executable, *sys.argv)


# load a json-textfile as a dict
def loadJsonFile(jsonFilename):
    jsonDataDict = None
    if os.path.exists(jsonFilename):
        with open(jsonFilename) as jsonfile:
            try:
                jsonDataDict = json.load( jsonfile )
            except Exception as err:
                print('ERROR LOADING FILE', jsonFilename, " >>> ", err)
    
    return jsonDataDict

    
# save a dict as a json-textfile
def saveJsonFile(jsonFilename, jsonDataDict):
    try:
        with open(jsonFilename, 'w') as jsonfile:
            json.dump(jsonDataDict, jsonfile, indent = 2)
        return True
    except Exception as err:
        print('ERROR SAVING FILE', jsonFilename, " >>> ", err)
        return False