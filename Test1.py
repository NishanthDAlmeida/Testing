import serial

import time

ser = serial.Serial('COM4', 9600)



def led_on():
    ser.write('a')


def led_off():
    ser.write('b')


time.sleep(5)

led_on()

print("done")
