from shift_register import shift_register_write, shift_register_set
from pinesp32 import SR_LED_L_BLUE, SR_LED_L_RED, SR_LED_L_GREEN, SR_LED_R_BLUE, SR_LED_R_GREEN, SR_LED_R_RED
from pinesp32 import SR_PT_BLUE, SR_PT_GREEN, SR_PT_RED, SR_PT_WHITE

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

def set_left_led(color: tuple[bool, bool, bool]):
    shift_register_set(SR_LED_L_RED, color[0])
    shift_register_set(SR_LED_L_GREEN, color[1])
    shift_register_set(SR_LED_L_BLUE, color[2])
    shift_register_write()

def set_right_led(color: tuple[bool, bool, bool]):
    shift_register_set(SR_LED_R_RED, color[0])
    shift_register_set(SR_LED_R_GREEN, color[1])
    shift_register_set(SR_LED_R_BLUE, color[2])
    shift_register_write()


###### lightsensorbar leds ######

def set_lightsensorbar_led(color: tuple[bool, bool, bool]):
    shift_register_set(SR_PT_RED, color[0])
    shift_register_set(SR_PT_GREEN, color[1])
    shift_register_set(SR_PT_GREEN, color[2])
    shift_register_write()

def set_lightsensorbar_white(state: bool):
    shift_register_set(SR_PT_WHITE, state)
    shift_register_write()
