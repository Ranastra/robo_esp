from shift_register import shift_register_write
from pinesp32 import SR_LED_L_BLUE, SR_LED_L_RED, SR_LED_L_GREEN, SR_LED_R_BLUE, SR_LED_R_GREEN, SR_LED_R_RED
# rgb leds: combining red, green and blue gives new colors
# turn led on by setting it to low


RED = (False, True, True)
BLUE = (True, True, False)
GREEN = (True, False, True)
WHITE = (False, False, False)
OFF = (True, True, True)
PURPLE = (False, True, False)
YELLOW = (False, False, True)
CYAN = (True, False, False)

def set_left_led(color:tuple[bool, bool, bool]):
    shift_register_write(SR_LED_L_RED, color[0])
    shift_register_write(SR_LED_L_GREEN, color[1])
    shift_register_write(SR_LED_L_BLUE, color[2])

def set_right_led(color:tuple[bool, bool, bool]):
    shift_register_write(SR_LED_R_RED, color[0])
    shift_register_write(SR_LED_R_GREEN, color[1])
    shift_register_write(SR_LED_R_BLUE, color[2])