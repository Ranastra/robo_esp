from pinesp32 import SERVO4
from machine import Pin
from servo_class import Servo
from time import sleep


servo = Servo(SERVO4)
servo.set(90)
sleep(1)
servo.set(0)
sleep(1)
servo.set(180)
sleep(1)
print("Done")
