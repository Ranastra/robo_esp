import pinesp32
import utime
import machine

# middle = machine.Pin(pinesp32.T_M, machine.Pin.IN, machine.Pin.PULL_DOWN)
left = machine.Pin(pinesp32.T_L, machine.Pin.IN,
                   machine.Pin.PULL_UP)  # is inverted
right = machine.Pin(pinesp32.T_R, machine.Pin.IN)

metal = machine.Pin(pinesp32.T_M, machine.Pin.IN) # silver ball sensor ... inverted


def test():
    while True:
        utime.sleep_ms(200)
        print("left", left.value(), end = "#")
        print("right", right.value(), end = "#")
        print("metal", metal.value())


if __name__ == "__main__":
    test()
