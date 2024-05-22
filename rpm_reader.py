import serial
from time import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

def get_rpm():
    start = time()
    while True:
        if time() - start > 0.5:
            return 0
        if ser.in_waiting > 0:
            try:
                rpm = float(ser.readline().decode('utf-8').rstrip())
            except UnicodeDecodeError as e:
                pass
            finally:
                rpm = 0
            return rpm
