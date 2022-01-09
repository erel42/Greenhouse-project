import os, shutil
import PySimpleGUI as sg


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


origin_path = ".\\App"
desired_path = ""

sg.theme('DarkAmber')

layout = [[sg.Text('ברוכים הבאים למתקין החממה!')],
          [sg.T(text=origin_path, k='-FILE_PATH-'),
           sg.Button(button_text='בחר תיקיית מקור', k='-FILE_SELECT-')],
          [sg.T(text=desired_path, k='-FILE_PATH2-'),
           sg.Button(button_text='בחר יעד התקנה, למשל שולחן העבודה', k='-FILE_SELECT-')],
          [sg.Button('התקן', k='-INSTALL-'), sg.Exit()]]

window = sg.Window('Window that stays open', layout)

while True:  # The Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'FILE_PATH':
        origin_file_path = sg.popup_get_file(message='בחר קובץ', title='Choose file', keep_on_top=True)
        if origin_file_path is not None:
            origin_path = origin_file_path
    elif event == 'FILE_PATH2':
        desired_file_path = sg.popup_get_file(message='בחר קובץ', title='Choose file', keep_on_top=True)
        if desired_file_path is not None:
            desired_path = desired_file_path
    elif event == '-INSTALL-':
        try:
            copytree(origin_path, desired_path)
            sg.popup_quick_message(title='ההתקנה הושלמה בהצלחה!')
        except:
            sg.popup_error(title='קרתה שגיאה!')


window.close()
