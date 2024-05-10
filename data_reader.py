import acc_module
import gps_recieve
from rpm_reader import get_rpm

mpu_enabled = True


logger = logging.getLogger(__name__)

try:
    mpu = acc_module.mpu()
except Exception as e:
    mpu_enabled = False

# On each data piece from gps get other data from sensors
for data in gps_recieve.gps():

    # Read data from mpu mpdule if it is enabled
    if mpu_enabled:
        temp = mpu.get_temp()
        accel = mpu.get_accel()
        gyro = mpu.get_gyro_data()
        data['acceleration'] = accel_data

    # Read data from arduino
    rpm = get_rpm()
    data['rpm'] = rpm

    # Set timestamp for datapiece
    data["date_time"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")

    data_json = json.dumps(data)
    try:
        a = requests.post('http://localhost:5000/sierra_data', json = data_json)
        logger.debug(a)
    except Exception as e:
        pass
    logger.debug(data)