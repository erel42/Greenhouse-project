import PySimpleGUI as sg
from datetime import datetime

# Define the window's contents
temp = hum = light = gHum = -1
column_names = [[sg.Text(text='לחות - אדמה', justification='center', size=(20, 2)),
                 sg.Text(text='אור', justification='center', size=(20, 2)),
                 sg.Text(text='לחות - אויר', justification='center', size=(20, 2)),
                 sg.Text(text='טמפרטורה', justification='center', size=(20, 2))]]

column_values = [[sg.Text(text='loading...', justification='center', k='-gHum-', size=(20, 2)),
                  sg.Text(text='loading...', justification='center', k='-light-', size=(20, 2)),
                  sg.Text(text='loading...', justification='center', k='-hum-', size=(20, 2)),
                  sg.Text(text='loading...', justification='center', k='-temp-', size=(20, 2))]]

column_light = [[sg.Input(default_text='0 - 255', justification='center', k='-BLUE-', size=(10, 2)),
                 sg.Text(text=':ירוק', justification='center', size=(5, 2)),
                 sg.Input(default_text='0 - 255', justification='center', k='-GREEN-', size=(10, 2)),
                 sg.Text(text=':כחול', justification='center', size=(5, 2)),
                 sg.Input(default_text='0 - 255', justification='center', k='-RED-', size=(10, 2)),
                 sg.Text(text=':אדום', justification='center', size=(5, 2)),
                 sg.Text(text=':תאורה', justification='center', size=(5, 2))]]

layout = [[sg.Text(text='Still loading...', key='-TIME-', justification='center')],
          [sg.Column(column_names, justification='center')],
          [sg.Column(column_values, justification='center')],
          [sg.Column(column_light, justification='center', vertical_alignment='center')],
          [sg.Text("What's your name?"), sg.Text("Hi")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40, 1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Greenhouse GUI', layout, resizable=True, element_justification='c')

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=1000)
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    elif event == 'Ok':
        window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

    window['-TIME-'].update(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    window['-hum-'].update(hum)
    window['-gHum-'].update(gHum)
    window['-light-'].update(light)
    window['-temp-'].update(temp)

# Finish up by removing from the screen
window.close()
