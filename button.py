import pinesp32
import time
import machine

# something wrong with T_L
left = machine.Pin(pinesp32.T_M, machine.Pin.IN, machine.Pin.PULL_DOWN)
right = machine.Pin(pinesp32.T_R, machine.Pin.IN, machine.Pin.PULL_DOWN)


def test():
    while True:
        time.sleep_ms(200)
        print("left", left.value())
        print("right", right.value())
