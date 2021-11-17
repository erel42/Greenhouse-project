import PySimpleGUI as sg
from datetime import datetime

# Great site: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#button-element

# Define the window's contents
temp = hum = light = gHum = ph = -1.0

# Faucet control
f_water = f_fertilizer = False



column_names = [
    [sg.Text(text='Ph', justification='center', font='david 30 normal', size=(10, 2), text_color='dark grey'),
     sg.Text(text='לחות - אדמה', justification='center', size=(10, 2), font='david 30 normal', text_color='brown'),
     sg.Text(text='אור', justification='center', font='david 30 normal', size=(10, 2), text_color='yellow'),
     sg.Text(text='לחות - אויר', justification='center', font='david 30 normal', size=(10, 2)),
     sg.Text(text='טמפרטורה', justification='center', font='david 30 normal', size=(10, 2), text_color='pink')],
    # New row, now we show values
    [sg.Text(text='loading...', justification='center', k='-PH-', font='david 30 normal', size=(10, 2),
             text_color='dark grey'),
     sg.Text(text='loading...', justification='center', k='-gHum-', font='david 30 normal', size=(10, 2),
             text_color='brown'),
     sg.Text(text='loading...', justification='center', k='-light-', font='david 30 normal', size=(10, 2),
             text_color='yellow'),
     sg.Text(text='loading...', justification='center', k='-hum-', font='david 30 normal', size=(10, 2)),
     sg.Text(text='loading...', justification='center', k='-temp-', font='david 30 normal', size=(10, 2),
             text_color='pink')]]

column_light = [[sg.Button(button_text='החל', font='david 30 normal'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-BLUE-', size=(10, 1),
                          default_text='0',
                          background_color='light blue', font='david 30 normal'),
                 sg.Text(text=':כחול', justification='center', size=(5, 1), text_color='light blue',
                         font='david 30 normal'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-GREEN-', size=(10, 1),
                          default_text='0',
                          background_color='light green', font='david 30 normal'),
                 sg.Text(text=':ירוק', justification='center', size=(5, 1), text_color='light green',
                         font='david 30 normal'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-RED-', size=(10, 1),
                          default_text='0',
                          background_color='red', font='david 30 normal'),
                 sg.Text(text=':אדום', justification='center', size=(5, 1), text_color='red', font='david 30 normal'),
                 sg.Text(text=':תאורה', justification='center', size=(5, 1), font='david 30 normal')]]

column_btnControls = [
    [sg.Button(k='-WATER-', image_filename='faucet-image-off.png', image_size=(150, 150),
               tooltip='לחצו כאן כדי לפתוח או לסגור את ברז המים', image_subsample=3),
     sg.Button(k='-FERTILIZER-', image_filename='fertilizer-png-off.png', image_size=(150, 150),
               tooltip='לחצו כאן כדי לפתוח או לסגור את ברז הדשן', image_subsample=3)]]

column_recording = [[sg.Button(image_filename='record-image.png', image_size=(100, 100), k='-RECORD-',
                               tooltip='לחצו כאן כדי להתחיל הקלטת נתונים', image_subsample=4),
                     sg.OptionMenu(values=["פעם בדקה", "פעם ב-5 דקות", "פעם ב-10 דקות"], s=30),
                     sg.Text(text=':תדירות הקלטה', font='david 30 normal'),
                     sg.Button(image_filename='upload-image.png', image_size=(100, 100), k='-UPLOAD-',
                               tooltip='לחצו כאן כדי לבחור תכנית פעולה')]]

column_heading = [
    [sg.Text(text='Still loading...', key='-TIME-', justification='center', font='david 30 normal', size=(10, 2),
             text_color='light grey'),
     sg.Text(text='בקרת חממה', justification='center', font='david 30 normal', size=(10, 2), text_color='light green')]]

column_exit = [[sg.Button(button_text='יציאה', font='david 30 normal', k='Quit')]]

layout = [[sg.Column(column_heading, justification='center')],
          [sg.Column(column_names, justification='center')],
          [sg.Column(column_light, justification='center', vertical_alignment='center')],
          [sg.Column(column_btnControls, justification='center', vertical_alignment='center')],
          [sg.Column(column_recording, justification='center', vertical_alignment='center')],
          [sg.Column(column_exit, justification='center', vertical_alignment='center')]]

# Create the window
window = sg.Window('Greenhouse GUI', layout, resizable=True, no_titlebar=True).Finalize()
window.Maximize()

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=300)
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-WATER-':
        f_water = not f_water
        if f_water:
            window['-WATER-'].update(image_filename='faucet-image-on.png', image_size=(150, 150),
                                     image_subsample=3)
        else:
            window['-WATER-'].update(image_filename='faucet-image-off.png', image_size=(150, 150),
                                     image_subsample=3)
    elif event == '-FERTILIZER-':
        f_fertilizer = not f_fertilizer
        if f_fertilizer:
            window['-FERTILIZER-'].update(image_filename='fertilizer-png-on.png', image_size=(150, 150),
                                          image_subsample=3)
        else:
            window['-FERTILIZER-'].update(image_filename='fertilizer-png-off.png', image_size=(150, 150),
                                          image_subsample=3)
    elif event == '-UPLOAD-':
        sg.popup_get_file(message='בחר תרחיש', title='Choose scenario')
    elif event == 'Quit':
        e_status = sg.popup_yes_no("האם אתם בטוחים שאתם רוצים לצאת? אם תצאו הקלטת הנתונים תיפסק", title='Exit screen')
        if e_status == 'Yes':
            break

    window['-TIME-'].update(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    window['-PH-'].update(ph)
    window['-hum-'].update(str(hum) + '%')
    window['-gHum-'].update(str(gHum) + '%')
    window['-light-'].update(str(light) + 'ADD UNIT')
    window['-temp-'].update(str(temp) + 'C')

# Finish up by removing from the screen
window.close()
