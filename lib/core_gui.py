# This python script uses the following encoding: utf8
import PySimpleGUI as sg

from lib import core_vars as var

#* ---------- BASIC GUI WINDOWS ----------

def showInfo(wintitle="Info", wintext=['Information',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1))])
    
    infowindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='center', keep_on_top=True, finalize=True)
    infowindow.BringToFront()
    event, values = infowindow.read()
    infowindow.close()
    
    if event == 'OK':
        return True
    else:
        return True # there is no false here ...

def getConfirmation(wintitle="Confirm", wintext=['Please confirm',]):
    layout = []
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))])
    
    confirmationwindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='center', keep_on_top=True, finalize=True)
    confirmationwindow.BringToFront()
    event, values = confirmationwindow.read()
    confirmationwindow.close()
    
    if event == 'OK':
        return True
    else:
        return False

def getMultipleChoice(wintitle="Please choose", wintext="Min 1 choice:", valuelist= ['none',], selectall=False):
    layout = [[sg.Text(wintext + ':')],]
    layout.append([sg.Text('')])
    for vitem in valuelist:
        layout.append([sg.Checkbox(vitem, default=selectall)])
    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))])
    
    choicewindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='left', keep_on_top=True, finalize=True)
    choicewindow.BringToFront()
    event, choices = choicewindow.read()
    choicewindow.close()
    
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

def getSingleChoice(wintitle="Please choose", wintext=["1 choice:"], valuelist= ['none',], selectfirst=False):
    layout = [] 
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([sg.Text('')])
    i=0
    for vitem in valuelist:
        i+=1
        if i==1 and selectfirst:
            layout.append([sg.Radio(vitem, 0, True)])
        else:
            layout.append([sg.Radio(vitem, 0)])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))])
    
    choicewindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='left', keep_on_top=True, finalize=True)
    choicewindow.BringToFront()
    event, choices = choicewindow.read()
    choicewindow.close()
    
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



def getSingleChoice_Dropdown(wintitle="Please choose", wintext=["1 choice:",], valuelist= ['none',], selectfirst=False):
    layout = [] 
    for text in wintext:
        layout.append([sg.Text(text)])
    
    layout.append([ sg.InputCombo(( valuelist ), font=('Courier New', 12), key='-choice-'),                ])

    layout.append([sg.Text('')])
    layout.append([sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))])
    
    choicewindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='center', keep_on_top=True, finalize=True)
    choicewindow.BringToFront()
    event, values = choicewindow.read()
    choicewindow.close()
    
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
                [sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))] ]
    
    filewindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='center', keep_on_top=True, finalize=True)
    filewindow.BringToFront()
    event, files = filewindow.read()
    filewindow.close()
    
    if event == 'OK':
        if files[0]:
            return files[0]
        else:
            showInfo('No File', ["No file selected"])
            return False
    else:
        return False

def getValue(wintitle="Value", wintext="Please ender value", defaulttext=''):
    

    layout = [] 
    for text in wintext:
        layout.append([sg.Text(text)])

    layout.append([
                [sg.Input(size=(40,1), default_text = defaulttext)],
                [sg.Text('')],
                [sg.OK(button_text='OK', button_color=('white', var.colors['green']), size=(22, 1)), sg.Cancel(button_text='CANCEL', button_color=('white', var.colors['red']), size=(23, 1))] 
        ])

    valuewindow = sg.Window(wintitle, layout, location=var.SETTINGS['window_position'], element_justification='center', keep_on_top=True, finalize=True)
    valuewindow.BringToFront()
    event, values = valuewindow.read()
    
    valuewindow.close()
    
    if event == 'OK':
        if values[0]:
            return values[0]
        else:
            #showInfo('Info', ["No Value entered"])
            return "" #False
    else:
        return False