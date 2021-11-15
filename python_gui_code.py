import PySimpleGUI as sg
import serial


def main():
    ser = serial.Serial('COM10', 9600, timeout=0, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=False,
                        rtscts=False,
                        write_timeout=None,
                        dsrdtr=False,
                        inter_byte_timeout=None,
                        exclusive=None)

    layout = [
        [sg.Text('A button to control the LED')],
        [sg.Button('LED off', size=(9, 4), button_color='white on red', key='-LED-'), sg.Button('Exit')]
    ]

    window = sg.Window('Green house GUI', layout)

    down = False
    while True:  # Event Loop
        if ser.inWaiting:
            print(ser.readline())
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == '-LED-':  # if the normal button that changes color and text
            down = not down
            window['-LED-'].update(text='LED on' if down else 'LED off',
                                   button_color='white on green' if down else 'white on red')
            if down:
                ser.write(bytes(b'1\n'))
            else:
                ser.write(bytes(b'2\n'))
    window.close()


if __name__ == '__main__':
    main()
