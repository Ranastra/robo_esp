from imu import MPU6050
import time
from machine import Pin, I2C
from pinesp32 import SCL, SDA


class Gyro():
    def __init__(self):
        i2c = I2C(1, sda=Pin(SDA), scl=Pin(SCL))
        self.imu = MPU6050(i2c)
        self.winkel = 0
        self.time = time.ticks_ms()
        self.x = 0
        self.y = 0
        (self.err_z, self.err_y, self.err_x) = self.calib()
        
    def reset(self):
        self.winkel = 0
        self.time = time.ticks_ms()
        
    def update(self):
        t = time.ticks_ms()
        dt= t - self.time
        self.time = t
        gz=self.imu.gyro.z
        gz = gz - self.err_z
        self.winkel += gz*dt/1000
        
    def update_stuff(self):
        t = time.ticks_ms()
        dt = t - self.time
        self.time = t
        gx = self.imu.gyro.x - self.err_x
        self.x += gx * dt/1000
        gy= self.imu.gyro.y - self.err_y
        self.y += gy * dt/1000
        
             
    def reset_stuff(self):
        self.x = 0
        self.y = 0
        self.time = time.ticks_ms()
        
    def calib(self):
        sum_z=0
        sum_x=0
        sum_y=0
        for _ in range(200):
           sum_z += self.imu.gyro.z
           sum_x += self.imu.gyro.x
           sum_y += self.imu.gyro.y
        err_z = sum_z/200
        err_y = sum_y/200
        err_x = sum_x/200
        print("gyro err_z:{", err_z, "}, err_y:{", err_y, "}, err_x:{", err_x, "}")
        return (err_z, err_y, err_x)
    
    def get_winkel(self):
        return self.winkel

def test_gyro():
    g = Gyro()
    while True:
        g.update()
        print(g.winkel)
        time.sleep(0.1)

test_gyro()