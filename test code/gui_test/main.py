import PySimpleGUI as S_gui
import serial
import warnings
import serial.tools.list_ports
from datetime import datetime

# Great site: https://pysimplegui.readthedocs.io/en/latest/call%20reference/#button-element

# Define the window's contents
temp = hum = light = gHum = ph = -1.0
red = green = blue = 0
prev_value = '#000000'
down = True

# Faucet control
f_water = f_fertilizer = False

# Establishing a connection with a connected arduino
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

ser = serial.Serial(arduino_ports[0], 9600, timeout=0, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    xonxoff=False,
                    rtscts=False,
                    write_timeout=None,
                    dsrdtr=False,
                    inter_byte_timeout=None,
                    exclusive=None)

# The sensor values row
column_names = [
    [S_gui.Text(text='Ph', justification='center', font='david 30 normal', size=(10, 2), pad=(10, 10),
                text_color='black'),
     S_gui.Text(text='לחות - אדמה', justification='center', size=(10, 2), pad=(14, 10), font='david 30 normal',
                text_color='black'),
     S_gui.Text(text='אור', justification='center', font='david 30 normal', size=(10, 2), pad=(12, 10),
                text_color='black'),
     S_gui.Text(text='לחות - אויר', justification='center', font='david 30 normal', size=(10, 2), pad=(12, 10),
                text_color='black'),
     S_gui.Text(text='טמפרטורה', justification='center', font='david 30 normal', size=(10, 2), pad=(14, 10),
                text_color='black')],
    # New row, now we show values
    [S_gui.Frame(title='', relief=S_gui.RELIEF_RAISED, background_color='grey', layout=[
        [S_gui.Text(text='loading...', justification='center', k='-PH-', font='david 30 normal', size=(10, 1),
                    text_color='black')]]),
     S_gui.Frame(title='', relief=S_gui.RELIEF_RAISED, background_color='grey', vertical_alignment='center', layout=[
         [S_gui.Text(text='loading...', justification='center', k='-gHum-', font='david 30 normal', size=(10, 1),
                     text_color='black')]]),
     S_gui.Frame(title='', background_color='grey', relief=S_gui.RELIEF_RAISED, layout=[
         [S_gui.Text(text='loading...', justification='center', k='-light-', font='david 30 normal', size=(10, 1),
                     text_color='black')]]),
     S_gui.Frame(title='', background_color='grey', relief=S_gui.RELIEF_RAISED, layout=[
         [S_gui.Text(text='loading...', justification='center', k='-hum-', font='david 30 normal', size=(10, 1),
                     text_color='black')]]),
     S_gui.Frame(title='', background_color='grey', relief=S_gui.RELIEF_RAISED, layout=[
         [S_gui.Text(text='loading...', justification='center', k='-temp-', font='david 30 normal', size=(10, 1),
                     text_color='black')]])]]

# The RGB controller row
column_light = [[S_gui.Button(button_text='החל', font='david 30 normal', k='-UPDATE-'),
                 S_gui.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-RED-', size=(10, 1),
                             default_text='0', background_color='red', font='david 30 normal'),
                 S_gui.Input(tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-GREEN-', size=(10, 1),
                             default_text='0', background_color='light green', font='david 30 normal'),
                 S_gui.Input(default_text='0', tooltip='הכניסו ערך בין 0 ל255', justification='center', k='-BLUE-',
                             size=(10, 1), background_color='light blue', font='david 30 normal'),
                 S_gui.Text(' או ', font='david 30 normal'),
                 S_gui.Input(default_text='#000000', visible=False, k='-C-'),
                 S_gui.ColorChooserButton('בחר צבע', image_filename='color.png', image_subsample=5, k='-COLOR-',
                                          target='-C-')]]

column_btnControls = [
    [S_gui.Button(k='-WATER-', image_filename='faucet-image-off.png', image_size=(150, 150),
                  tooltip='לחצו כאן כדי לפתוח או לסגור את ברז המים', image_subsample=3),
     S_gui.Button(k='-FERTILIZER-', image_filename='fertilizer-png-off.png', image_size=(150, 150),
                  tooltip='לחצו כאן כדי לפתוח או לסגור את ברז הדשן', image_subsample=3)]]

column_exit = [[S_gui.Button(button_text='יציאה', font='david 30 normal', k='Quit')]]

column_recording = [[S_gui.Button(image_filename='record-image.png', image_size=(150, 150), k='-RECORD-',
                                  tooltip='לחצו כאן כדי להתחיל הקלטת נתונים', image_subsample=3),
                     S_gui.OptionMenu(values=["פעם בדקה", "פעם ב-5 דקות", "פעם ב-10 דקות"], s=30),
                     S_gui.Text(text=':תדירות', font='david 30 normal'),
                     S_gui.Button(image_filename='upload-image.png', image_size=(150, 150), k='-UPLOAD-',
                                  tooltip='לחצו כאן כדי לבחור תכנית פעולה')]]

layout = [[S_gui.Column(
    [[S_gui.Text(text='Still loading...', key='-TIME-', justification='left', font='david 16 normal', size=(10, 2),
                 text_color='light grey')]], expand_x=True),
    S_gui.Button(k='-SETTINGS-', image_filename='settings-png.png', image_size=(50, 50), tooltip='הגדרות',
                 image_subsample=10)],
    [S_gui.Column([[S_gui.Text(text='בקרת חממה', justification='center', font='david 44 normal', size=(10, 1),
                               text_color='yellow')]], justification='center', vertical_alignment='center',
                  pad=(7, 15))],
    [S_gui.Column([[S_gui.Frame(vertical_alignment='center', title_location=S_gui.TITLE_LOCATION_TOP_RIGHT,
                                font='david 30 normal', title=':ערכי חיישנים',
                                layout=[
                                    [S_gui.Column(column_names, justification='center',
                                                  vertical_alignment='center')]])]], justification='center',
                                pad=(7, 7))],
    [S_gui.Column([[S_gui.Frame(vertical_alignment='center', title_location=S_gui.TITLE_LOCATION_TOP_RIGHT,
                                font='david 30 normal', title=':תאורה', layout=[
            [S_gui.Column(column_light, justification='center', vertical_alignment='center')]])]],
                  justification='center', pad=(7, 7))],
    [S_gui.Column([[S_gui.Frame(vertical_alignment='center', title_location=S_gui.TITLE_LOCATION_TOP_RIGHT,
                                font='david 30 normal', title=':בקרת ברזים', layout=[
            [S_gui.Column(column_btnControls, justification='center', vertical_alignment='center')]]),
                    S_gui.Frame(vertical_alignment='center', title_location=S_gui.TITLE_LOCATION_TOP_RIGHT,
                                font='david 30 normal', title=':אפשרויות הפעלה והקלטה', layout=[
                            [S_gui.Column(column_recording, justification='center', vertical_alignment='center')]])]],
                  justification='center', pad=(7, 7))],
    [S_gui.Column(column_exit, vertical_alignment='center', justification='left')]]

# Create the window
window = S_gui.Window('Greenhouse GUI', layout, resizable=True, no_titlebar=True, keep_on_top=True).Finalize()
window.Maximize()

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=300)
    # See if user wants to quit or window was closed
    if event == S_gui.WINDOW_CLOSED:
        break
    elif event == '-WATER-':
        f_water = not f_water
        if f_water:
            window['-WATER-'].update(image_filename='faucet-image-on.png', image_size=(150, 150),
                                     image_subsample=3)
            ser.write(bytes(b'3\n'))
        else:
            window['-WATER-'].update(image_filename='faucet-image-off.png', image_size=(150, 150),
                                     image_subsample=3)
            ser.write(bytes(b'4\n'))
    elif event == '-FERTILIZER-':
        f_fertilizer = not f_fertilizer
        if f_fertilizer:
            window['-FERTILIZER-'].update(image_filename='fertilizer-png-on.png', image_size=(150, 150),
                                          image_subsample=3)
            ser.write(bytes(b'5\n'))
        else:
            window['-FERTILIZER-'].update(image_filename='fertilizer-png-off.png', image_size=(150, 150),
                                          image_subsample=3)
            ser.write(bytes(b'6\n'))
    elif event == '-UPLOAD-':
        S_gui.popup_get_file(message='בחר תרחיש', title='Choose scenario', keep_on_top=True)

    elif event == '-SETTINGS-':
        S_gui.popup_cancel(title='Need to switch into settings window', keep_on_top=True)

    elif event == '-UPDATE-':
        if prev_value != values['-C-']:
            prev_value = values['-C-']
            print('Hello ' + prev_value)
            tempString = ""
            tempString += prev_value[1]
            tempString += prev_value[2]
            red = int(tempString, 16)
            tempString = ""
            tempString += prev_value[3]
            tempString += prev_value[4]
            green = int(tempString, 16)
            tempString = ""
            tempString += prev_value[5]
            tempString += prev_value[6]
            blue = int(tempString, 16)
            window['-BLUE-'].update(blue)
            window['-RED-'].update(red)
            window['-GREEN-'].update(green)
        else:
            red = values['-RED-']
            blue = values['-BLUE-']
            green = values['-GREEN-']
        ser.write(bytes(('c ' + str(red) + ' ' + str(green) + ' ' + str(blue) + '\n').encode('utf8', 'strict')))

    elif event == 'Quit':
        e_status = S_gui.popup_yes_no("האם אתם בטוחים שאתם רוצים לצאת? אם תצאו הקלטת הנתונים תיפסק",
                                      title='Exit screen', keep_on_top=True)
        if e_status == 'Yes':
            break

    window['-TIME-'].update(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    window['-PH-'].update(ph)
    window['-hum-'].update(str(hum) + '%')
    window['-gHum-'].update(str(gHum) + '%')
    window['-light-'].update(str(light) + ' LUX')
    window['-temp-'].update(str(temp) + 'C')

    # Handle serial communications
    if ser.inWaiting:
        print(ser.readline())
# Finish up by removing from the screen
window.close()
