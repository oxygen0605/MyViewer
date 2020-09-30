# -*- coding: utf-8 -*-
"""

"""


import PySimpleGUI as sg
#import subprocess



###### Model
def read_text_file(values):
    try:
        with open(values["filename"], 'r', encoding='utf-8') as f:
            text = f.read()
            state = "updated"
    except Exception as e:
        text = e
        state = "error"

    return state, text

def save_text_file(values):
    try:
        with open(values["filename"]+".txt", 'w', encoding='utf-8') as f:
            f.write(window['text_box'].Get())
            text = "This file is saved at "+ values["filename"].split()[-1]
            state = "saved"
    except Exception as e:
        text = e
        state = "error"
    return state, text

def is_file_exists(values):
    from os import path
    
    if path.isfile(values["filename"]):
        text = "This file is existing. Would you overwrite it?"
        state = "confirm_overwrite"
    else :
        text = "saving"
        state = "saving"

    return state, text

###### View
memu_bar = [sg.Text("ファイル"), 
                 sg.InputText(size=(75,1), key="filename"), 
                 sg.FileBrowse("選択", key="select", target="filename"), 
                 sg.Submit("読込",key='notify_read'), sg.Button("保存", key="notify_save")]
text_frame = [sg.Frame('テキスト内容',[[sg.Output(size=(100,15),key='text_box')]])]
log_frame = [sg.Frame('ログ出力',[[sg.Output(size=(100,10),key='log_box')]])]
main_layout = [memu_bar, text_frame, log_frame]
window = sg.Window(title='Text Viewer',layout=main_layout)

def update_text_box(text):
    window['text_box'].update(text)
    return 'idle'

def update_log_box(text):
    window['log_box'].update(text)
    return 'idle'

def clear_text_box(text):
    window['text_box'].update([])
    return 'idle'

def clear_log_box(text):
    window['log_box'].update([])
    return 'idle'

def exe_save_popup(text):
    popup_layout = [[sg.Text(text)], [sg.Button("OK", key="notify_ok"), sg.Button("Cancel", key="notify_cancel")]]
    popup_window = sg.Window(title='Save Confirmation',layout=popup_layout)
    event, values = popup_window.read()

    if event in ('notify_cancel', None):
        status = "idle"
    else:
        status = "saving"

    popup_window.close()
    return status

##### Presenter
event_handler = {
        'notify_read':[read_text_file],
        'notify_save':[is_file_exists],
        'save_file':[save_text_file]
        }

view_handler = {
        'idle'   :[],
        'updated':[update_text_box, clear_log_box],
        'confirm_overwrite':[exe_save_popup],
        'saved':[update_log_box],
        'error'  :[update_log_box, clear_text_box]
        }

while True:
    state = "idle"
    event, values = window.read()

    if event in ('Exit', 'Quit', None):
        state = 'finished'
        break
    
    while True:
        # operation model functions
        functions = event_handler[event]
        for f in functions:
            state,text = f(values)

        # View Update
        view_functions = view_handler[state]
        for f in view_functions:
            state = f(text)

        if state == 'saving':
            event = 'save_file'

        if state in ('idle', 'updated', 'saved', 'error'):
            break


window.close()




