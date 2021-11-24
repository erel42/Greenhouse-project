import PySimpleGUI as sg
import serial
from datetime import datetime

# Great site: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#button-element

# Define the window's contents
temp = hum = light = gHum = ph = -1.0
red = green = blue = 0
picker = False
down = True

# Faucet control
f_water = f_fertilizer = False

ser = serial.Serial('COM9', 9600, timeout=0, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=False,
                        rtscts=False,
                        write_timeout=None,
                        dsrdtr=False,
                        inter_byte_timeout=None,
                        exclusive=None)

column_names = [
    [sg.Text(text='Ph', justification='center', font='david 30 normal', size=(10, 2), pad=(10, 10), text_color='black'),
     sg.Text(text='לחות - אדמה', justification='center', size=(10, 2), pad=(14, 10), font='david 30 normal',
             text_color='black'),
     sg.Text(text='אור', justification='center', font='david 30 normal', size=(10, 2), pad=(12, 10),
             text_color='black'),
     sg.Text(text='לחות - אויר', justification='center', font='david 30 normal', size=(10, 2), pad=(12, 10),
             text_color='black'),
     sg.Text(text='טמפרטורה', justification='center', font='david 30 normal', size=(10, 2), pad=(14, 10),
             text_color='black')],
    # New row, now we show values
    [sg.Frame(title='', relief=sg.RELIEF_RAISED, background_color='grey', layout=[
        [sg.Text(text='loading...', justification='center', k='-PH-', font='david 30 normal', size=(10, 1),
                 text_color='black')]]),
     sg.Frame(title='', relief=sg.RELIEF_RAISED, background_color='grey', vertical_alignment='center', layout=[
         [sg.Text(text='loading...', justification='center', k='-gHum-', font='david 30 normal', size=(10, 1),
                  text_color='black')]]),
     sg.Frame(title='', background_color='grey', relief=sg.RELIEF_RAISED, layout=[
         [sg.Text(text='loading...', justification='center', k='-light-', font='david 30 normal', size=(10, 1),
                  text_color='black')]]),
     sg.Frame(title='', background_color='grey', relief=sg.RELIEF_RAISED, layout=[
         [sg.Text(text='loading...', justification='center', k='-hum-', font='david 30 normal', size=(10, 1),
                  text_color='black')]]),
     sg.Frame(title='', background_color='grey', relief=sg.RELIEF_RAISED, layout=[
         [sg.Text(text='loading...', justification='center', k='-temp-', font='david 30 normal', size=(10, 1),
                  text_color='black')]])]]

column_light = [[sg.Button(button_text='החל', font='david 30 normal', k='-UPDATE-'),
                 sg.Input(default_text='0', tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-BLUE-',
                          size=(10, 1), background_color='light blue', font='david 30 normal'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-GREEN-', size=(10, 1),
                          default_text='0', background_color='light green', font='david 30 normal'),
                 sg.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-RED-', size=(10, 1),
                          default_text='0', background_color='red', font='david 30 normal'),
                 sg.Text(' או ', font='david 30 normal'),
                 sg.Text('#000000', font='david 30 normal', visible=False, k='-C-'),
                 sg.ColorChooserButton('בחר צבע', image_filename='color.png', image_subsample=5, k='-COLOR-', target='-C-')]]

column_btnControls = [
    [sg.Button(k='-WATER-', image_filename='faucet-image-off.png', image_size=(150, 150),
               tooltip='לחצו כאן כדי לפתוח או לסגור את ברז המים', image_subsample=3),
     sg.Button(k='-FERTILIZER-', image_filename='fertilizer-png-off.png', image_size=(150, 150),
               tooltip='לחצו כאן כדי לפתוח או לסגור את ברז הדשן', image_subsample=3)]]

column_exit = [[sg.Button(button_text='יציאה', font='david 30 normal', k='Quit')]]

column_recording = [[sg.Button(image_filename='record-image.png', image_size=(150, 150), k='-RECORD-',
                               tooltip='לחצו כאן כדי להתחיל הקלטת נתונים', image_subsample=3),
                     sg.OptionMenu(values=["פעם בדקה", "פעם ב-5 דקות", "פעם ב-10 דקות"], s=30),
                     sg.Text(text=':תדירות', font='david 30 normal'),
                     sg.Button(image_filename='upload-image.png', image_size=(150, 150), k='-UPLOAD-',
                               tooltip='לחצו כאן כדי לבחור תכנית פעולה')]]

layout = [[sg.Column(
    [[sg.Text(text='Still loading...', key='-TIME-', justification='left', font='david 16 normal', size=(10, 2),
              text_color='light grey')]], expand_x=True),
    sg.Button(k='-SETTINGS-', image_filename='settings-png.png', image_size=(50, 50), tooltip='הגדרות',
              image_subsample=10)],
    [sg.Column([[sg.Text(text='בקרת חממה', justification='center', font='david 44 normal', size=(10, 1),
                         text_color='yellow')]], justification='center', vertical_alignment='center',
               pad=(7, 15))],
    [sg.Column([[sg.Frame(vertical_alignment='center', title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                          font='david 30 normal', title=':ערכי חיישנים', layout=[
            [sg.Column(column_names, justification='center', vertical_alignment='center')]])]],
               justification='center', pad=(7, 7))],
    [sg.Column([[sg.Frame(vertical_alignment='center', title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                          font='david 30 normal', title=':תאורה', layout=[
            [sg.Column(column_light, justification='center', vertical_alignment='center')]])]],
               justification='center', pad=(7, 7))],
    [sg.Column([[sg.Frame(vertical_alignment='center', title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                          font='david 30 normal', title=':בקרת ברזים', layout=[
            [sg.Column(column_btnControls, justification='center', vertical_alignment='center')]]),
                 sg.Frame(vertical_alignment='center', title_location=sg.TITLE_LOCATION_TOP_RIGHT,
                          font='david 30 normal', title=':אפשרויות הפעלה והקלטה', layout=[
                         [sg.Column(column_recording, justification='center', vertical_alignment='center')]])]],
               justification='center', pad=(7, 7))],
    [sg.Column(column_exit, vertical_alignment='center', justification='left')]]

# Create the window
window = sg.Window('Greenhouse GUI', layout, resizable=True, no_titlebar=True, keep_on_top=True).Finalize()
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
        sg.popup_get_file(message='בחר תרחיש', title='Choose scenario', keep_on_top=True)

    elif event == '-SETTINGS-':
        sg.popup_cancel(title='Need to switch into settings window', keep_on_top=True)

    elif event == '-UPDATE-':
        if picker:
            window['-BLUE-'].update(blue)
            window['-RED-'].update(red)
            window['-GREEN-'].update(green)
            picker = False
        else:
            red = values['-RED-']
            blue = values['-BLUE-']
            green = values['-GREEN-']

    elif event == 'COLOR':
        picker = True

    elif event == 'Quit':
        e_status = sg.popup_yes_no("האם אתם בטוחים שאתם רוצים לצאת? אם תצאו הקלטת הנתונים תיפסק", title='Exit screen',
                                   keep_on_top=True)
        if e_status == 'Yes':
            break

    window['-TIME-'].update(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    window['-PH-'].update(ph)
    window['-hum-'].update(str(hum) + '%')
    window['-gHum-'].update(str(gHum) + '%')
    window['-light-'].update(str(light) + ' LUX')
    window['-temp-'].update(str(temp) + 'C')

    #Handle serial communications
    if ser.inWaiting:
        print(ser.readline())
# Finish up by removing from the screen
window.close()
