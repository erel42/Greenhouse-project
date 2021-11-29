import PySimpleGUI as sg
import time

file1 = open('test.txt', 'r')

Lines = file1.readlines()
count = 0
lCount = 0
pause = 0
current_time = time.time()
# red = green = blue = 0
_red = _green = _blue = 0
file = []
faucets = ['ברז 1', 'ברז 2']
modes = ['לפי זמן', 'לפי ערך']
parameters = ['אור', 'לחות באויר', 'לחות באדמה', 'טמפרטורה']
_type = ['-גדול מ', '-קטן מ']

parameters_dic = {
    'אור': 'light',
    'לחות באויר': 'hum',
    'לחות באדמה': 'gHum',
    'טמפרטורה': 'temp'
}

_type_dic = {
    '-גדול מ': '>',
    '-קטן מ': '<'
}

linesOnScreen = 10
debug = True  # Set to True to print comments

for i in range(1, linesOnScreen + 1):
    file.append('')


def printLine(line_count, _line):
    window['-TXT-'].update("Line{}: {}".format(line_count, _line.strip()))


def applyScenario():
    global pause
    global count
    if pause <= current_time:
        line = Lines[count]
        count += 1
        while line[0] == '#' and not debug:
            if count >= len(Lines):
                count = 0
            line = Lines[count]
            count += 1
        if line[0] == '#' or line[0] == '@':
            printLine(count, line)
        elif line[0] == 'd':
            line = line[2:]
            pause = current_time + float(line)
        elif line[0] == 'c':
            line = line[2:]
            line = line[:-1]
            window['-F' + line + '-'].update('Faucet' + line + ' is close')
        elif line[0] == 'o':
            line = line[2:]
            line = line[:-1]
            window['-F' + line + '-'].update('Faucet' + line + ' is open')
        elif line[0] == 's':
            line = line[2:]
            window['-C-'].update("Color: {}".format(line.strip()))

        if count >= len(Lines):
            count = 0


def lightPopup(index):
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
    file[index - 1] = 's ' + str(_red) + ' ' + str(_green) + ' ' + str(_blue)
    window['-Text' + str(index) + '-'].update(
        'משנה את הצבע ל: אדום-' + str(_red) + ' ירוק-' + str(_green) + ' כחול-' + str(_blue))


def faucetPopup(index):
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
    window['-Text' + str(index) + '-'].update(str_to_show)


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
    window['-Text' + str(index) + '-'].update(str_to_show)


sg.theme('DarkAmber')  # Keep things interesting for your users

layout = [[sg.Button('Faucet1 is close', k='-F1-')],
          [sg.Button('Faucet2 is close', k='-F2-')],
          [sg.Text('Color: 0 0 0', k='-C-')],
          [sg.Text('Persistent window', k='-TXT-')],
          [sg.Button('צור קובץ', k='-CREATE-'), sg.Button('Add line', k='-LINE-'), sg.Exit()]]

# Generating input lines
for i in range(1, linesOnScreen + 1):
    layout.append([sg.Text(str(i) + ': ', k='-Line' + str(i) + '-', size=(5, 1)),
                   sg.DropDown(['ברזים', 'תאורה', 'השהייה'], k='-Header' + str(i) + '-'),
                   sg.Button('הגדר', k='CONF' + str(i)),
                   sg.Text('', k='-Text' + str(i) + '-')])

window = sg.Window('Window that stays open', layout, font='david 18 normal').finalize()
# window.maximize()

while True:  # The Event Loop
    event, values = window.read(timeout=50)
    current_time = time.time()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-CREATE-':
        status, pop_values = sg.Window('בחירת שם', [[sg.T('בחרו שם קובץ')],
                                                    [sg.Input(default_text='Scenario', k='-NAME-'),
                                                     sg.Button('החל', s=10), sg.Button('בטל', s=10)]],
                                       disable_close=True).read(close=True)
        file_write = open(pop_values['-NAME-'] + '.txt', 'w')
        for i in range(0, len(file)):
            file_write.write(file[i] + '\n')
        file_write.close()
    elif 'CONF' in event:
        test = values['-Header' + event[-1] + '-']
        if int(event[-1]) > 1 and file[int(event[-1]) - 2] == '':
            sg.popup_error('נא להגדיר פעולות על פי סדר!')
        elif test == 'ברזים':
            faucetPopup(int(event[-1]))
        elif test == 'תאורה':
            lightPopup(int(event[-1]))
        elif test == 'השהייה':
            delayPopup(int(event[-1]))
        else:
            sg.popup_error('נא להכניס ערך תקין')

    applyScenario()
