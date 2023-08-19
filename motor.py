import math
import shift_register
import pinesp32
import machine
import time

print("motor got started")

Mot = int
MOT_A: Mot = 1
MOT_B: Mot = 2
MOT_AB: Mot = 3
_PWMA: machine.PWM = machine.PWM(machine.Pin(pinesp32.PWMA))
_PWMB: machine.PWM = machine.PWM(machine.Pin(pinesp32.PWMB))


def drive(mot: Mot, speed: int):
    direction = speed < 0
    speed = int(min(math.fabs(speed), 100))
    shift_register.set(pinesp32.SR_STBY, True)
    if mot & MOT_A:  # IN1 and IN2 are switched or inverted?
        shift_register.set(pinesp32.SR_AIN1, direction)
        shift_register.set(pinesp32.SR_AIN2, not direction)
        _PWMA.duty_u16(speed * 655)  # 100*655 ~ 16bit
    if mot & MOT_B:
        shift_register.set(pinesp32.SR_BIN1, direction)
        shift_register.set(pinesp32.SR_BIN2, not direction)
        _PWMB.duty_u16(speed * 655)
    shift_register.write()


def drive_stop(mot: Mot):
    if mot & MOT_A:
        _PWMA.duty_u16(0)
    if mot & MOT_B:
        _PWMB.duty_u16(0)


def test_drive():
    """test drive forward backward 5 times"""
    time.sleep(5)
    for _ in range(5):
        drive(MOT_AB, 80)
        time.sleep(2)
        drive(MOT_AB, -80)
        time.sleep(2)
    drive_stop(MOT_AB)
