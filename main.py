import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import app
from flask import Response
from flask import Flask
from flask import request
from datetime import datetime
import time
import os
import json
import pytz
import logging

app = Flask("data_writer")
token = "h36wa8NITjKnTxXb0DXP-zdMzTSPdVZWcJUgvo9PjS0-vLk3ny0mAQYcXKuacu2Yz8xoUyP_DvInDXEV99Wwew=="
org = "test"
url = "http://localhost:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket = "test2"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

logger = logging.getLogger(__name__)

@app.route('/sierra_data', methods=['POST'])
def write_data_to_db():
  logger.debug(request.json)
  data = json.loads(request.json)
  point_dict = {
    "measurement": "telemetry",
    "tags": {"car": "sierra"},
    "fields": {},
    "time": 0
  }
  fields = {}
  date = data.get('date_time')
  date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.UTC)

  coordinates = data.get('coordinates', [0,0,0])
  fields['x'] = coordinates[0]
  fields['y'] = coordinates[1]
  fields['z'] = coordinates[2]

  fields['throttle'] = data.get('rpm', 0)

  acc = data.get('acceleration', [0, 0, 0])

  fields['acceleration_x'] = acc[0]
  fields['acceleration_y'] = acc[1]
  fields['acceleration_z'] = acc[2]

  point_dict['fields'] = fields
  point_dict['time'] = date

  point = Point.from_dict(point_dict)
  write_api.write(bucket=bucket, org="test", record=point)
  return "200"

if __name__ == '__main__':
  try:
    app.run(debug=True, host='localhost', port=5000)
  except Exception as e:
    logger.exception(e)
  finally:
    write_client.close()