import PySimpleGUI as sg
import time


count = 0
lCount = 0
pause = 0
offset = 0
max_offset = 0
current_time = time.time()
_red = _green = _blue = 0
flow = 1.0  # Liters per hour
file = []
shouts = []
pre = ['10']
faucets = ['ברז 1', 'ברז 2']
modes = ['לפי זמן', 'לפי ערך', 'לפי ספיקות']
parameters = ['אור', 'לחות באויר', 'לחות באדמה', 'טמפרטורה']
_type = ['-גדול מ', '-קטן מ']

parameters_dic = {
    'אור': 'light',
    'לחות באויר': 'humidity',
    'לחות באדמה': 'moisture',
    'טמפרטורה': 'temp'
}

_type_dic = {
    '-גדול מ': '>',
    '-קטן מ': '<'
}

linesOnScreen = 15
debug = True  # Set to True to print comments

for i in range(1, linesOnScreen + 1):
    file.append('')
    shouts.append('')


def generateSettings():
    global flow
    success = False
    while not success:
        status, pop_values = sg.Window('הגדרות נוספות',
                                       [[sg.Input(default_text='10'), sg.T(':תדירות הקלטה בדקות')],
                                        [sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                       disable_close=True, element_justification='Right').read(close=True)
        if status == 'בטל':
            return
        try:
            int(pop_values[0])
            pre[0] = pop_values[0]
            break
        except:
            sg.popup_error('קלא לא תקין!')
    print(pre[0])


def cycleBackLines(_values, _window):
    global offset, max_offset, shouts, file
    offset -= 1
    for i in range(2, linesOnScreen + 1):
        _window['-Header' + str(i) + '-'].update(values['-Header' + str(i - 1) + '-'])
        _window['-Line' + str(i) + '-'].update(': ' + str(i + offset))
        window['-Text' + str(i) + '-'].update(shouts[i + offset - 1])
    try:
        if file[offset][0] == 'o':
            _window['-Header1-'].update('ברזים')
        elif file[offset][0] == 's':
            _window['-Header1-'].update('תאורה')
        elif file[offset][0] == 'd':
            _window['-Header1-'].update('השהייה')
        else:
            _window['-Header1-'].update('')
    except:
        _window['-Header1-'].update('')
    _window['-Line1-'].update(': ' + str(offset + 1))
    _window['-Text1-'].update(shouts[offset])


def cycleLines(_values, _window):
    global offset, max_offset, shouts
    offset += 1
    if offset > max_offset:
        max_offset += 1
        file.append('')
        shouts.append('')
    for i in range(1, linesOnScreen):
        _window['-Header' + str(i) + '-'].update(values['-Header' + str(i + 1) + '-'])
        _window['-Line' + str(i) + '-'].update(': ' + str(i + offset))
        window['-Text' + str(i) + '-'].update(shouts[i + offset - 1])
    _window['-Header' + str(linesOnScreen) + '-'].update('')
    _window['-Line' + str(linesOnScreen) + '-'].update(': ' + str(linesOnScreen + offset))
    _window['-Text' + str(linesOnScreen) + '-'].update('')


def printLine(line_count, _line):
    window['-TXT-'].update("Line{}: {}".format(line_count, _line.strip()))


def lightPopup(index):
    str_to_send = ''
    str_to_show = ''
    global _red, _green, _blue
    success = False
    while not success:
        status, pop_values = sg.Window('הגדרת צבעים',
                                       [[sg.T('אנא בחר ערכי צבעים')],
                                        [sg.Input(default_text='0'), sg.T(':כחול'), sg.Input(default_text='0'),
                                         sg.T(':ירוק'),
                                         sg.Input(default_text='0'), sg.T(':אדום'), sg.Button('החל', s=10),
                                         sg.Button('בטל', s=10)]],
                                       disable_close=True).read(close=True)
        if status == 'בטל':
            return
        try:
            int(pop_values[0])
            int(pop_values[1])
            int(pop_values[2])
        except:
            sg.popup_error('יש להקליד מספרים בין 0 ל255 בלבד!')
            continue
        _red = int(pop_values[2])
        _green = int(pop_values[1])
        _blue = int(pop_values[0])
        if _red >= 0 and _green >= 0 and _blue >= 0 and _red <= 255 and _green <= 255 and _blue <= 255:
            success = True
        else:
            sg.popup_error('יש להקליד מספרים בין 0 ל255 בלבד!')
    str_to_send = 's ' + str(_red) + ' ' + str(_green) + ' ' + str(_blue)
    str_to_show = 'משנה את הצבע ל: אדום-' + str(_red) + ' ירוק-' + str(_green) + ' כחול-' + str(_blue)
    file[index - 1] = str_to_send
    window['-Text' + str(index - offset) + '-'].update(str_to_show)
    shouts[index - 1] = str_to_show


def faucetPopup(index):
    global flow
    success = False
    mode = ''
    f_number = 0
    str_to_send = ''
    str_to_show = ''
    _time = 0
    while not success:

        status, pop_values = sg.Window('בקרת ברזים',
                                       [[sg.DropDown(modes, k='-MODE-'),
                                         sg.T(' :בחר אופן תפעול'), sg.DropDown(faucets, k='-FNUMBER-'),
                                         sg.T(' :אנא בחר ברז'), sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                       disable_close=True).read(close=True)
        if status == 'בטל':
            return
        if pop_values['-FNUMBER-'] in faucets and pop_values['-MODE-'] in modes:
            mode = pop_values['-MODE-']
            f_number = pop_values['-FNUMBER-']
            break
        sg.popup_error('אנא הכניסו ערכים תקינים')

    faucet = f_number[-1]
    success = False
    if mode == 'לפי ערך':
        while not success:
            status, pop_values = sg.Window('בחירת תנאי',
                                           [[sg.T('בחרו משתנה ומתי יפעל')],
                                            [sg.Input(k='-VALUE-'), sg.DropDown(_type, k='-TYPE-'), sg.T('כל עוד הוא'),
                                             sg.DropDown(parameters, k='-PARA-'), sg.T(' :בחר משתנה'),
                                             sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                           disable_close=True).read(close=True)
            if status == 'בטל':
                return
            if pop_values['-TYPE-'] in _type and pop_values['-PARA-'] in parameters:
                try:
                    int(pop_values['-VALUE-'])
                    str_to_send = 'o ' + faucet + ' v ' + parameters_dic[pop_values['-PARA-']] + ' ' + _type_dic[
                        pop_values['-TYPE-']] + ' ' + pop_values['-VALUE-']
                    str_to_show = 'פותח את ברז ' + faucet + ' כל עוד ' + pop_values['-PARA-'] + ' יהיה ' + \
                                  pop_values['-TYPE-'][1:] + ' ' + pop_values['-VALUE-']
                    break
                except:
                    sg.popup_error('אנא הכניסו ערכים תקינים')
                    continue
            sg.popup_error('אנא הכניסו ערכים תקינים')
    elif mode == 'לפי ספיקות':
        while not success:
            _flow = 0
            status, pop_values = sg.Window('בחירת ספיקות',
                                           [[sg.T('בחרו כמות מים רצויה בסמק')],
                                            [sg.Input(default_text='0', k='-FLOW-'),
                                             sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                           disable_close=True).read(close=True)
            if status == 'בטל':
                return
            try:
                _flow = int(pop_values['-FLOW-'])
                str_to_send = 'o ' + faucet + ' f ' + str(_flow)
                str_to_show = 'פותח את ברז ' + faucet + ' על מנת שיזרמו ' + str(_flow) + ' סמק של מים'
                break
            except:
                sg.popup_error('אנא הכניסו ערכים תקינים')
    else:
        while not success:
            status, pop_values = sg.Window('בחירת זמן',
                                           [[sg.T('בחרו למשך כמה זמן הברז יהיה פתוח')],
                                            [sg.Input(default_text='0', k='-SECS-'), sg.T(':שניות'),
                                             sg.Input(default_text='0', k='-MINS-'), sg.T(':דקות'),
                                             sg.Input(default_text='0', k='-HOURS-'), sg.T(':שעות'),
                                             sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                           disable_close=True).read(close=True)
            if status == 'בטל':
                return
            try:
                _time += int(pop_values['-HOURS-']) * 3600
                _time += int(pop_values['-MINS-']) * 60
                _time += int(pop_values['-SECS-'])
                str_to_send = 'o ' + faucet + ' t ' + str(_time)
                str_to_show = 'פותח את ברז ' + faucet + ' למשך ' + str(_time) + ' שניות'
                break
            except:
                sg.popup_error('אנא הכניסו ערכים תקינים')

    file[index - 1] = str_to_send
    window['-Text' + str(index - offset) + '-'].update(str_to_show)
    shouts[index - 1] = str_to_show


def delayPopup(index):
    str_to_send = ''
    str_to_show = ''
    _time = 0
    success = False
    while not success:
        status, pop_values = sg.Window('בחירת זמן', [[sg.T('בחרו זמן השהייה')],
                                                     [sg.Input(default_text='0', k='-SECS-'), sg.T(':שניות'),
                                                      sg.Input(default_text='0', k='-MINS-'), sg.T(':דקות'),
                                                      sg.Input(default_text='0', k='-HOURS-'), sg.T(':שעות'),
                                                      sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                       disable_close=True).read(close=True)
        if status == 'בטל':
            return
        try:
            _time += int(pop_values['-HOURS-']) * 3600
            _time += int(pop_values['-MINS-']) * 60
            _time += int(pop_values['-SECS-'])
            str_to_send = 'd ' + str(_time)
            str_to_show = 'השהייה למשך ' + str(_time) + ' שניות'
            break
        except:
            sg.popup_error('אנא הכניסו ערכים תקינים')

    file[index - 1] = str_to_send
    window['-Text' + str(index - offset) + '-'].update(str_to_show)
    shouts[index - 1] = str_to_show


sg.theme('DarkAmber')  # Keep things interesting for your users

layout = [[sg.Text('Color: 0 0 0', k='-C-', visible=False)],
          [sg.Text('Persistent window', k='-TXT-', visible=False)],
          [sg.Button('צור קובץ', k='-CREATE-')],
          [sg.Button('הגדרות נוספות', k='-ADDITIONALINFO-'), sg.Button('גלגל מעלה', k='-LINE-'),
           sg.Button('גלגל מטה', k='-LINEBACK-'), sg.Exit()]]

# Generating input lines
for i in range(1, linesOnScreen + 1):
    layout.append([sg.Text('', k='-Text' + str(i) + '-'),
                   sg.Button('הגדר', k='CONF' + str(i)),
                   sg.DropDown(['ברזים', 'תאורה', 'השהייה'], k='-Header' + str(i) + '-'),
                   sg.Text(': ' + str(i), k='-Line' + str(i) + '-', size=(5, 1), justification='right')])

window = sg.Window('יצירת קובץ אוטומטי', layout, font='david 18 normal', element_justification='right').finalize()
window.maximize()

while True:  # The Event Loop
    event, values = window.read(timeout=50)
    current_time = time.time()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Exit':
        e_status = sg.popup_yes_no("האם אתם בטוחים שאתם רוצים לצאת?", title='Exit screen', keep_on_top=True)
        if e_status == 'Yes':
            break
    elif event == '-CREATE-':
        status, pop_values = sg.Window('בחירת שם', [[sg.T('בחרו שם קובץ')],
                                                    [sg.Input(default_text='Scenario', k='-NAME-'),
                                                     sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                       disable_close=True).read(close=True)
        if status == 'בטל':
            continue
        working = False
        while not working:
            working = True
            try:
                file_write = open(".\\scenarios\\" + pop_values['-NAME-'] + '.txt', 'w', encoding="utf-8")
            except:
                working = False
        file_write.write('{\n')
        for i in range(0, len(pre)):
            file_write.write(pre[i])
            file_write.write('\n')
        file_write.write('}\n')
        for i in range(0, len(file)):
            if file[i] != '':
                file_write.write('@ ' + shouts[i] + '\n')
                file_write.write(file[i] + '\n')
        file_write.close()
    elif 'CONF' in event:
        test = values['-Header' + event[-1] + '-']
        if (int(event[-1]) + offset) > 1 and file[int(event[-1]) + offset - 2] == '':
            sg.popup_error('נא להגדיר פעולות על פי סדר!')
        elif test == 'ברזים':
            faucetPopup(int(event[-1]) + offset)
        elif test == 'תאורה':
            lightPopup(int(event[-1]) + offset)
        elif test == 'השהייה':
            delayPopup(int(event[-1]) + offset)
        else:
            sg.popup_error('נא להכניס ערך תקין')
    elif event == '-LINE-':
        cycleLines(values, window)
    elif event == '-LINEBACK-':
        if offset > 0:
            cycleBackLines(values, window)
    elif event == '-ADDITIONALINFO-':
        generateSettings()
