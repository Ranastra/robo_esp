from imu import MPU6050
import time
from machine import Pin, I2C
from pinesp32 import SCL, SDA


# number of sensor readings taken for calibration
_SAMPLE_CALIB = 200
# bumper is active for 2 seconds
# _BUMPER_ON_TIME = 2_000
# bumper is active when 5 degrees are reached
# _BUMPER_ACTIVATION_ANGLE = 5


class _Gyro():
    def __init__(self):
        i2c = I2C(1, sda=Pin(SDA, Pin.PULL_UP), scl=Pin(SCL, Pin.PULL_UP), freq=400000)
        self.__imu = MPU6050(i2c)
        self.__angle = 0.
        self.__time = time.ticks_ms()
        self.__x = 0.0
        self.__y = 0.0
        (self.__err_z, self.__err_y, self.__err_x) = self.calib()
        self.__active = False
        self.__active_count = 0

    def active(self) -> bool:
        if self.__active:
            self.update()
            self.__active_count += 1
            if self.__active_count > 60:
                self.__active = False
        return self.__active

    def set_active(self):
        self.__active = True
        self.__active_count = 0

    def reset(self):
        self.__angle = 0
        self.__time = time.ticks_ms()

    def update(self):
        t = time.ticks_ms()
        dt = t - self.__time
        self.__time = t
        gz = self.__imu.gyro.z
        gz = gz - self.__err_z
        self.__angle += gz * dt / 1000

    def update_x_y(self):
        t = time.ticks_ms()
        dt = t - self.__time
        self.__time = t
        gx = self.__imu.gyro.x - self.__err_x
        self.__x += gx * dt / 1000
        gy = self.__imu.gyro.y - self.__err_y
        self.__y += gy * dt / 1000

    def reset_x_y(self):
        self.__x = 0
        self.__y = 0
        self.time = time.ticks_ms()

    def calib(self) -> tuple[float, float, float]:
        sum_z = 0.0
        sum_x = 0.0
        sum_y = 0.0
        for _ in range(_SAMPLE_CALIB):
            sum_z += self.__imu.gyro.z
            sum_x += self.__imu.gyro.x
            sum_y += self.__imu.gyro.y
        err_z = sum_z / _SAMPLE_CALIB
        err_y = sum_y / _SAMPLE_CALIB
        err_x = sum_x / _SAMPLE_CALIB
        return (err_z, err_y, err_x)

    def get_angle(self) -> float:
        return self.__angle

    def get_x(self) -> float:
        return self.__x


gyro = _Gyro()

def test_gyro():
    # Test gyro Werte
    print("In Gyro test1")
    gyro.reset()
    while True:
        gyro.update()
        print(gyro.get_angle())


# class Bumper():
#     def __init__(self):
#         """ is supposed to be used as if the object is a bool """
#         self.__enabled = False
#         self.__time = time.ticks_ms()

#     def __update(self):
#         """ update gyro and checks for activation angle or timeout of bumper active """
#         gyro.update_x_y()
#         if abs(gyro.get_x) > _BUMPER_ACTIVATION_ANGLE:
#             # if print_mode:
#             #     print("bumper on")
#             gyro.reset_x_y()
#             self.__enabled = True
#             self.__time = time.ticks_ms()
#         else:
#             if self.__enabled and (
#                     self.__time + _BUMPER_ON_TIME) < time.ticks_ms():
#                 # if print_mode:
#                 #     print("bumper off")
#                 self.__enabled = False

#     def __bool__(self) -> bool:
#         self.__update()
#         return self.__enabled


#bumper = Bumper()
