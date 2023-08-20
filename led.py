import shift_register
import pinesp32
import time

# rgb leds: combining red, green and blue gives new colors
# turn led on by setting it to low


###### status leds ######
color = tuple[bool, bool, bool]

RED:    color = (False, True,  True)
BLUE:   color = (True,  True,  False)
GREEN:  color = (True,  False, True)
WHITE:  color = (False, False, False)
OFF:    color = (True,  True,  True)
PURPLE: color = (False, True,  False)
YELLOW: color = (False, False, True)
CYAN:   color = (True,  False, False)


def set_status_left(color: color):
    """set color of left status LED"""
    shift_register.set(pinesp32.SR_LED_L_RED, color[0])
    shift_register.set(pinesp32.SR_LED_L_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_L_BLUE, color[2])
    shift_register.write()


def set_status_right(color: color):
    """set color of right status LED"""
    shift_register.set(pinesp32.SR_LED_R_RED, color[0])
    shift_register.set(pinesp32.SR_LED_R_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_R_BLUE, color[2])
    shift_register.write()


###### lightsensorbar leds ######

def set_lightsensorbar_rgb(color: color):
    """set color of status LED on lightsensorbar"""
    shift_register.set(pinesp32.SR_PT_RED, not color[0])
    shift_register.set(pinesp32.SR_PT_GREEN, not color[1])
    shift_register.set(pinesp32.SR_PT_BLUE, not color[2])
    shift_register.write()


def set_lightsensorbar_white(state: bool):
    """toggle white LEDs on lightsensorbar"""
    shift_register.set(pinesp32.SR_PT_WHITE, state)
    shift_register.write()


def test_status():
    """cycle through all colors for the status LEDs"""
    colors = [RED, BLUE, GREEN, WHITE, OFF, PURPLE, YELLOW, CYAN]
    while True:
        for color in colors:
            set_status_left(color)
            set_status_right(color)
            time.sleep_ms(500)
