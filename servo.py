import machine
import time
import pinesp32


# Für den SG90 wurden folgende Pulslängen empirisch bestimmt:
# 0°    400us
# 90°   1400us
# 180°  2400us

class Servo:
    def __init__(self, pin, min_us=400, max_us=2200):

        # Servo wird mit PWM signal mit Fequenz 50Hz gesteuert
        # -> Periodendauer 20ms = 20000us
        # -> Puls-Pausenverhältnis (duty cycle) wird über 16-Bit-Wert (0...65535) gesteuert

        self.pwm = machine.PWM(machine.Pin(pin))
        self.pwm.freq(50)

        # Berechnung von min und max duty-cycle aus den uerbergebenen Pulslängen in ms
        #   val_us        20000us
        #   ------   =   -------
        #   duty          65535

        self.duty_min = (min_us*65535)//20000
        self.duty_max = (max_us*65535)//20000

        # Fuer die Umrechnung winkel nach duty cycle wird eine Geradengleichung
        #   y= mx + n
        # verwendet
        #  n = duty_min
        #  m  = (self.duty_max-self.duty_min)//180
        self.delta_duty = self.duty_max-self.duty_min

    def set(self, winkel):
        self.pwm.duty_u16((self.delta_duty*winkel)//180 + self.duty_min)

    def off(self):
        self.pwm.duty_u16(0)


def test(servo_pin=pinesp32.SERVO1):
    servo = Servo(servo_pin, min_us=450, max_us=2200)
    while True:
        servo.set(0)
        print(0)
        time.sleep(1)
        servo.set(90)
        print(90)
        time.sleep(1)
        servo.set(180)
        print(180)
        time.sleep(1)
