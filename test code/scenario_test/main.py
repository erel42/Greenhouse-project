import PySimpleGUI as sg
import time

file1 = open('scenario.txt', 'r')

Lines = file1.readlines()
count = 0
pause = 0
current_time = time.time()
debug = True  # Set to True to print comments


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


sg.theme('DarkAmber')  # Keep things interesting for your users

layout = [[sg.Button('Faucet1 is close', k='-F1-')],
          [sg.Button('Faucet2 is close', k='-F2-')],
          [sg.Text('Color: 0 0 0', k='-C-')],
          [sg.Text('Persistent window', k='-TXT-')],
          [sg.Button('Read', k='-READ-'), sg.Exit()]]

window = sg.Window('Window that stays open', layout)

while True:  # The Event Loop
    event, values = window.read(timeout=50)
    current_time = time.time()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-READ-':
        pause = 0
    applyScenario()
