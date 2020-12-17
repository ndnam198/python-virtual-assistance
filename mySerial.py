import serial
import keyboard

with serial.Serial(port="COM21", baudrate=115200, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE) as ser:
    keyboard.add_hotkey('1', lambda: ser.write(b"help\r"))
    keyboard.add_hotkey('2', lambda: ser.write(b"time\r"))
    keyboard.add_hotkey('3', lambda: ser.write(b"process\r"))
    keyboard.add_hotkey('4', lambda: ser.write(b"reboot\r"))
    ser.close()
    ser.open()
    while True:
        if(ser.in_waiting > 0):
            serial_string = ser.read(100)
            print(serial_string.decode('Ascii'), end='')
            # ser.write(b"help\r")
