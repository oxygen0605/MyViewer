# -*- coding: utf-8 -*-
"""

"""


import PySimpleGUI as sg
#import subprocess

###### Model
def read_text_file(values):
    try:
        with open(values["input1"], 'r', encoding='utf-8') as f:
            text = f.readlines()
            state = "updated"
    except Exception as e:
        text = [e]
        state = "error"

    return state, text

def save_text_file(values):
    state = "error"
    text = ["Save cmd is unimplemented."]
    return state, text

###### View
memu_bar = [sg.Text("ファイル"), 
                 sg.InputText(key="input1"), 
                 sg.FileBrowse("選択", key="selecter1", target="input1"), 
                 sg.Submit("読込",key='reader1'), sg.Button("保存", key="save_text")]
text_frame = [sg.Frame('テキスト内容',[[sg.Listbox([], size=(100,15),key='text_box')]])]
log_frame = [sg.Frame('ログ出力',[[sg.Listbox([], size=(100,10),key='log_box')]])]
main_layout = [memu_bar, text_frame, log_frame]
window = sg.Window(title='Text Viewer',layout=main_layout)

def update_text_box(text: list):
    window['text_box'].update(text)

def update_log_box(text: list):
    window['log_box'].update(text)

def clear_text_box(text: list):
    window['text_box'].update([])

def clear_log_box(text: list):
    window['log_box'].update([])


##### Presenter
model_handler = {
        'reader1': read_text_file,
        'save_text':save_text_file
        }
view_handler = {
        'idle'   :[],
        'updated':[update_text_box, clear_log_box],
        'error'  :[update_log_box, clear_text_box]
        }

while True:
    state = "idle"
    event, values = window.read()
    
    if event in ('Exit', 'Quit', None):
        break
    
    # call model function
    model_function = model_handler[event]
    state,text = model_function(values)

    # View Update
    view_functions = view_handler[state]
    for f in view_functions:
        f(text)

window.close()

