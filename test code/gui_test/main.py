import PySimpleGUI as sg
from datetime import datetime

# Great site: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#button-element

# Define the window's contents
temp = hum = light = gHum = ph = -1.0
column_names = [[sg.Text(text='חומציות', justification='center', font='david 30 normal', size=(10, 2)),
                 sg.Text(text='לחות - אדמה', justification='center', size=(10, 2), font='david 30 normal'),
                 sg.Text(text='אור', justification='center', font='david 30 normal', size=(10, 2)),
                 sg.Text(text='לחות - אויר', justification='center', font='david 30 normal', size=(10, 2)),
                 sg.Text(text='טמפרטורה', justification='center', font='david 30 normal', size=(10, 2))]]

column_values = [[sg.Text(text='loading...', justification='center', k='-PH-', font='david 30 normal', size=(10, 2)),
                  sg.Text(text='loading...', justification='center', k='-gHum-', font='david 30 normal', size=(10, 2)),
                  sg.Text(text='loading...', justification='center', k='-light-', font='david 30 normal', size=(10, 2)),
                  sg.Text(text='loading...', justification='center', k='-hum-', font='david 30 normal', size=(10, 2)),
                  sg.Text(text='loading...', justification='center', k='-temp-', font='david 30 normal', size=(10, 2))]]

column_light = [[sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-BLUE-', size=(10, 1)),
                 sg.Text(text=':כחול', justification='center', size=(5, 1), text_color='light blue'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-GREEN-', size=(10, 1)),
                 sg.Text(text=':ירוק', justification='center', size=(5, 1), text_color='light green'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-RED-', size=(10, 1)),
                 sg.Text(text=':אדום', justification='center', size=(5, 1), text_color='red'),
                 sg.Text(text=':תאורה', justification='center', size=(5, 1))]]

column_btnControls = [[sg.Button(button_text='השקיה', k='-WATER-', button_color="white on red", font='david 30 normal',
                                 tooltip='הפעילו את ההשקיה'),
                       sg.Button(button_text='   דשן   ', k='-FERTILIZER-', font='david 30 normal',
                                 button_color="white on red", tooltip='הפעילו את הדשן')]]

column_recording = [[sg.OptionMenu(values=["פעם בדקה", "פעם ב-5 דקות", "פעם ב-10 דקות"]),
                     sg.Text(text=':תדירות הקלטה', font='david 30 normal'),
                     sg.Button(image_filename='upload-image.png', image_size=(100, 100), k='-UPLOAD-',
                               tooltip='לחצו כאן כדי לבחור תכנית פעולה')]]

layout = [
    [sg.Text(text='Still loading...', key='-TIME-', justification='center', font='david 30 normal', size=(10, 2))],
    [sg.Column(column_names, justification='center')],
    [sg.Column(column_values, justification='center')],
    [sg.Column(column_light, justification='center', vertical_alignment='center')],
    [sg.Column(column_btnControls, justification='center', vertical_alignment='center')],
    [sg.Column(column_recording, justification='center', vertical_alignment='center')],
    [sg.Text("What's your name?"), sg.Text("Hi")],
    [sg.Input(key='-INPUT-')],
    [sg.Text(size=(40, 1), key='-OUTPUT-')],
    [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Greenhouse GUI', layout, resizable=True, element_justification='c', no_titlebar=True).Finalize()
window.Maximize()

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=500)
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    elif event == 'Ok':
        window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

    window['-TIME-'].update(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    window['-PH-'].update(ph)
    window['-hum-'].update(str(hum) + '%')
    window['-gHum-'].update(str(gHum) + '%')
    window['-light-'].update(str(light) + 'ADD UNIT')
    window['-temp-'].update(str(temp) + 'C')

# Finish up by removing from the screen
window.close()
