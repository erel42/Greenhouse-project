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
    finished = False
    input_s = ""
    input_e = ""
    input_f = ""
    finished = False
    ser.write(bytes(b'1\n'))
    while not finished:
        while ser.inWaiting():
            input_s = ser.readline()
            input_e = input_s.decode('utf8', 'strict')
            input_f += input_e
            i = 0
            while i < len(input_e):
                if (input_e[i] == ']'):
                    finished = True
                i = i + 1

    input_f = input_f[1:]
    input_f = input_f.replace(']', '')
    input_f = input_f.replace('\n', '')
    print(input_f)
    f = open("demofile2.csv", "a")
    f.write(input_f)
    f.close()

    #with open('records.csv', 'w', newline='') as file:
        #writer = csv.writer(file)
        #writer.writerow()#############
        #writer.writerow([1, "cool", "Frodo Baggins"])
        #writer.writerow([2, "Harry Potter", "Harry Potter"])

    with open('demofile2.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

main()