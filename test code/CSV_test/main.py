import serial
import csv


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
    ser.readline()
    data = ""
    ser.write(bytes(b'1'))
    leave = False
    while not leave:
        if len(data) > 3:
            if data[2] == 'H':
                leave = True
        else:
            data = ser.readline()
    print('data is here!')
    print(data)
    with open('records.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        writer.writerow([1, "cool", "Frodo Baggins"])
        writer.writerow([2, "Harry Potter", "Harry Potter"])

    with open('records.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

main()