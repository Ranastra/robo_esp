import pinesp32
import utime
import machine
import adc_multi

# middle = machine.Pin(pinesp32.T_M, machine.Pin.IN, machine.Pin.PULL_DOWN)
left = machine.Pin(pinesp32.T_L, machine.Pin.IN,
                   machine.Pin.PULL_UP)  # is inverted
right = machine.Pin(pinesp32.T_R, machine.Pin.IN, machine.Pin.PULL_UP)

# metal = machine.Pin(pinesp32.T_M, machine.Pin.IN) # silver ball sensor ... inverted

def read_metal()-> bool:
    adc_multi.set_channel(pinesp32.ADC_T_M)
    return adc_multi.read_like_button() < 4095


def test():
    while True:
        utime.sleep_ms(200)
        print("left", left.value(), end = "#")
        print("right", right.value(), end = "#")
        print("metal", read_metal())


if __name__ == "__main__":
    test()
