import os
import shutil
import PySimpleGUI as sg
import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0)


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

layout = [[sg.Text('!ברוכים הבאים למתקין החממה')],
          [sg.T(k='-PATH-'),
           sg.Button(button_text='בחר תיקיית מקור', k='-FOLDER_SELECT-')],
          [sg.T(k='-PATH2-'),
           sg.Button(button_text='בחר יעד התקנה', k='-FOLDER_SELECT2-')],
          [sg.Button('התקן', k='-INSTALL-'), sg.Exit()]]

window = sg.Window('Greenhouse installer', layout, element_justification='right', size=(500, 150), resizable=True)

while True:  # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-FOLDER_SELECT-':
        origin_file_path = sg.popup_get_folder(message='בחר תיקייה', title='Choose folder', keep_on_top=True)
        if origin_file_path is not None:
            origin_path = origin_file_path
            window['-PATH-'].update(origin_path)
    elif event == '-FOLDER_SELECT2-':
        desired_file_path = sg.popup_get_folder(message='בחר תיקייה', title='Choose folder', keep_on_top=True)
        if desired_file_path is not None:
            desired_path = desired_file_path
            window['-PATH2-'].update(desired_path)
    elif event == '-INSTALL-':
        try:
            copytree(origin_path, desired_path)
            sg.popup_quick_message(title='ההתקנה הושלמה בהצלחה!')
        except:
            sg.popup_error(title='קרתה שגיאה!')


window.close()
