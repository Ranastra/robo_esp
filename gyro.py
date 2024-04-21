import machine
import utime
import i2c
import imu

##### gyro #####

_CALIB_NUMBER = 200  # number of measurements for calibration


_imu = imu.MPU6050(i2c.I2C)
_utime = utime.ticks_ms()

angle = [0.0, 0.0, 0.0]
_err = [0.0, 0.0, 0.0]


# def get_tilt():
#     _imu._write

def reset():
    """reset angles and utimestamp"""
    global angle, _utime
    angle = [0.0, 0.0, 0.0]
    _utime = utime.ticks_ms()


def update():
    """get readings and update angle"""
    global _utime
    current_utime = utime.ticks_ms()
    delta_utime = _utime - current_utime
    _utime = current_utime
    angle[0] += (_imu.gyro.x - _err[0]) * delta_utime / 1000
    angle[1] += (_imu.gyro.y - _err[1]) * delta_utime / 1000
    angle[2] += (_imu.gyro.z - _err[2]) * delta_utime / 1000


def calib():
    global _err
    sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
    for _ in range(_CALIB_NUMBER):
        sum_x += _imu.gyro.x
        sum_y += _imu.gyro.y
        sum_z += _imu.gyro.z
    _err = [
        sum_x / _CALIB_NUMBER,
        sum_y / _CALIB_NUMBER,
        sum_z / _CALIB_NUMBER
    ]
    reset()


##### gyro active counters #####
_MAX_ACTIVE_TIME_MS: int = 500
_active: bool = False
_active_utimestamp: int = utime.ticks_ms()


def active_update():
    """update gyro and make sure that the angle is reseted from utime to utime"""
    global _active, _active_utimestamp
    if not _active:
        _active = True
        _active_utimestamp = utime.ticks_ms()
        reset()
    else:
        update()
        if _active_utimestamp + _MAX_ACTIVE_TIME_MS < utime.ticks_ms():
            _active = False

#### tests ####

def get_tilt() -> float:
    return _imu.accel.x



def test():
    reset()
    calib()
    print(_err)
    while True:
        for _ in range(10):
            update()
        print(angle)

def test_accell_gyro():
    while True:
        print('accel', _imu.accel.x, _imu.accel.y, _imu.accel.z)
        print('gyroo', _imu.gyro.x, _imu.gyro.y, _imu.gyro.z)
        utime.sleep_ms(400)
        

if __name__ == '__main__':
    test_accell_gyro()
