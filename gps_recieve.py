import socket
import requests
import json
from datetime import datetime

# Set socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 29998))

def gps() -> dict:
    """
    Method returns dict with gps data like this:
    {'coordinates': [latitude: float, longtitude: float], 'gps_speed': speed_in_km/h: float}
    :return:
    """
    while True:
        # Recieve data from socket
        msg_received = sock.recv(128)
        msg_received = msg_received.decode("UTF-8")
        msg = msg_received.split(',')
        print(msg_received)
        lng = '0'
        lat = '0'
        speed = '0'
        if msg[0][3:] == "GGA" or msg[0][3:] == "GNS":
            lng = msg[2].replace('.', '')
            lng = lng.lstrip('0')
            lng = lng[:2] + '.' + lng[2:]
            lat = msg[4].replace('.', '')
            lat = lat.lstrip('0')
            lat = lat[:2] + '.' + lat[2:]
        if msg[0][3:] == "VTG":
            speed = msg[7]
        elif msg[0][3:] == "DHV":
            speed = msg[6]*3.6
        coords = f"lng = {lng}, lat = {lat}"
        if lng != '0' or speed != '0':
            data = {'coordinates': [float(lat), float(lng)], 'gps_speed': float(speed)}
            yield data
        else:
            data = {'coordinates': [float(0), float(0)], 'gps_speed': float(0)}
            yield data
