import serial
from time import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
                print(type(rpm))
                return rpm
            except UnicodeDecodeError as e:
                logger.debug(e, exc_info=True)
