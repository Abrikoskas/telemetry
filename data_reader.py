from datetime import datetime
import gps_recieve
import requests
import logging
import json
import time

mpu_enabled = True
rpm_enabled = True

# import acc_module
# mpu = acc_module.Mpu()

url = 'http://localhost:5000/sierra_data'
# url = 'http://http://192.168.1.80:5000/sierra_data'


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

try:
    from rpm_reader import get_rpm
except Exception as e:
    logger.warning(e, exc_info=True)
    rpm_enabled = False
    logger.debug('rpm_enabled = False')

# On each data piece from gps get other data from sensors
for data in gps_recieve.gps():
    # Read data from mpu mpdule if it is enabled
    # if mpu_enabled:
    #     temp = mpu.get_temp()
    #     time.sleep(0.1)
    #     accel = mpu.get_accel()
    #     time.sleep(0.1)
    #     gyro = mpu.get_gyro()
    #     data['acceleration'] = accel

    if rpm_enabled == True:
        # Read data from arduino
        rpm = get_rpm()
        data['rpm'] = rpm

    # Set timestamp for datapiece
    data["date_time"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    data_json = json.dumps(data)
    try:
        a = requests.post(url, json = data_json)
        logger.debug(a)
    except Exception as e:
        logger.exception(e, exc_info=True)
    logger.debug(data)
