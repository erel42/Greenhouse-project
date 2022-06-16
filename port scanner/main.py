import serial  # Check if needed
import serial.tools.list_ports
import time

if __name__ == '__main__':
    for p in serial.tools.list_ports.comports():
        print('device: ' + p.device + ', description: ' + p.description)
    time.sleep(8)
