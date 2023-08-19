import shift_register
import pinesp32
import time

# rgb leds: combining red, green and blue gives new colors
# turn led on by setting it to low


###### status leds ######

RED = (False, True, True)
BLUE = (True, True, False)
GREEN = (True, False, True)
WHITE = (False, False, False)
OFF = (True, True, True)
PURPLE = (False, True, False)
YELLOW = (False, False, True)
CYAN = (True, False, False)


def set_status_left(color: tuple[bool, bool, bool]):
    shift_register.set(pinesp32.SR_LED_L_RED, color[0])
    shift_register.set(pinesp32.SR_LED_L_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_L_BLUE, color[2])
    shift_register.write()


def set_status_right(color: tuple[bool, bool, bool]):
    shift_register.set(pinesp32.SR_LED_R_RED, color[0])
    shift_register.set(pinesp32.SR_LED_R_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_R_BLUE, color[2])
    shift_register.write()


###### lightsensorbar leds ######

def set_lightsensorbar_rgb(color: tuple[bool, bool, bool]):
    shift_register.set(pinesp32.SR_PT_RED, not color[0])
    shift_register.set(pinesp32.SR_PT_GREEN, not color[1])
    shift_register.set(pinesp32.SR_PT_BLUE, not color[2])
    shift_register.write()


def set_lightsensorbar_white(state: bool):
    shift_register.set(pinesp32.SR_PT_WHITE, state)
    shift_register.write()


def test_status():
    colors = [RED, BLUE, GREEN, WHITE, OFF, PURPLE, YELLOW, CYAN]
    while True:
        for color in colors:
            set_status_left(color)
            set_status_right(color)
            time.sleep_ms(500)
