import machine
import time
import i2c
import imu

_CALIB_NUMBER = 200  # number of measurements for calibration


_imu = imu.MPU6050(i2c.I2C)
_time = time.ticks_ms()

angle = [0.0, 0.0, 0.0]
_err = [0.0, 0.0, 0.0]


def reset():
    global angle, _time
    angle = [0.0, 0.0, 0.0]
    _time = time.ticks_ms()


def update():
    global _time
    current_time = time.ticks_ms()
    delta_time = _time - current_time
    _time = current_time
    angle[0] += (_imu.gyro.x - _err[0]) * delta_time / 1000
    angle[1] += (_imu.gyro.y - _err[1]) * delta_time / 1000
    angle[2] += (_imu.gyro.z - _err[2]) * delta_time / 1000


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


def test():
    reset()
    calib()
    print(_err)
    while True:
        for _ in range(10):
            update()
        print(angle)
