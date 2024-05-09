import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

def get_rpm():
    while True:
        if ser.in_waiting > 0:
            rpm = float(ser.readline().decode('utf-8').rstrip())
            return rpm
