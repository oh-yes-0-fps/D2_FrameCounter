import PySimpleGUI as sg


from Stability import gui_comp as stability_gui
from Reload import gui_comp as reload_gui

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

sg.theme('DarkBlue')   # Add a touch of color

# All the stuff inside your window.
layout = [  [sg.Text('Choose a script to run')],
            [sg.Button('Exit')] ]


# Create the Window


script_idx = 0
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):   # if user closes window or clicks cancel
        break

window.close()

