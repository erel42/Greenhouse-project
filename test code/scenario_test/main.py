import PySimpleGUI as sg

sg.theme('DarkAmber')  # Keep things interesting for your users

file1 = open('scenario.txt', 'r')

layout = [[sg.Text('Persistent window')],
          [sg.Button('Read', k='-READ-'), sg.Exit()]]

window = sg.Window('Window that stays open', layout)

Lines = file1.readlines()
count = 0

while True:  # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-READ-':
        line = Lines[count]
        count += 1
        print("Line{}: {}".format(count, line.strip()))
        if count >= len(Lines):
            count = 0
