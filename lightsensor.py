from adc_multi import read_raw_adc, set_channel
import pinesp32 as p
import led
import time
from sensor import all_sensors, green_sensors, red_sensors, Sensor


###### Level for colors ######
_WHITE_LEVEL:int = const(0)
_DARK_LEVEL:int = const(0)
_RED_GREEN_DIFF_GREEN_LEVEL:int = const(0)
_RED_GREEN_DIFF_RED_LEVEL:int = const(0)
_WHITE_LEVEL_GREEN:int = const(0)

###### colors ######
COLOR = int
GREEN:COLOR = const(2)
BLACK:COLOR = const(1)
WHITE:COLOR = const(0)
RED:COLOR = const(3)
SILVER:COLOR = const(4)

###### directions ######
DIRECTION = int
FORWARD:DIRECTION = const(0)
LEFT:DIRECTION = const(1)
RIGHT:DIRECTION = const(-1)
BACKWARD:DIRECTION = const(3)

###### measure functions ######

def measure_white():
    led.set_lightsensorbar_white(True)
    for sens in all_sensors:
        set_channel(sens.channel)
        sens.val = read_raw_adc()
    led.set_lightsensorbar_white(False)


def measure_green_red() -> list[int]:
    led.set_lightsensorbar_led(led.GREEN)
    for sens in green_sensors:
        set_channel(sens.channel)
        sens.val = read_raw_adc()
    led.set_lightsensorbar_led(led.RED)
    for sens in red_sensors:
        set_channel(sens.channel)
        sens.val = read_raw_adc()
    led.set_lightsensorbar_led(led.OFF)


###### line follower functions ######

def all_white() -> bool:
    for sens in all_sensors:
        if sens.map_raw_value() < _WHITE_LEVEL:
            return False
    return True

def outer_see_dark() -> bool:
    return all_sensors[0].val < _DARK_LEVEL or all_sensors[-1] < _DARK_LEVEL

def get_linefollower_diff() -> float:
    diff_outside = all_sensors[0].val - all_sensors[6].val
    diff_middle = all_sensors[1].val - all_sensors[5].val
    diff_inside = all_sensors[2].val - all_sensors[4].val
    diff = diff_inside + diff_middle * 1.5 + diff_outside * 2
    return diff

def decide_crossroad(values: list[list[COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """
    l = values[0]
    r = values[1]
    lg = 0
    rg = 0
    if l[0] == GREEN and l[1] == BLACK:
        lg = 1
    if r[0] == GREEN and r[1] == BLACK:
        rg = 1
    if lg == 1 and rg == 1:
        return BACKWARD
    elif lg == 1:
        return LEFT
    elif rg == 1:
        return RIGHT
    else:
        return FORWARD


###### green filters ######

class _GreenFilter():
    def __init__(self, outer_sens_green:Sensor, inner_sens_green:Sensor, outer_sens_red:Sensor, inner_sens_red:Sensor):
        self._outer_sens_green = outer_sens_green
        self._inner_sens_green = inner_sens_green
        self._outer_sens_red = outer_sens_red
        self._inner_sens_red = inner_sens_red
        self._count_no_green = 0
        self._count_green = 0
        self._green = False
        self._count_red = 0

    def get_color(self) -> COLOR:
        green = (self._inner_sens_green.val + self._outer_sens_green.val) // 2
        red = (self._inner_sens_red.val + self._inner_sens_red.val) // 2
        if green - red > _RED_GREEN_DIFF_GREEN_LEVEL:
            self._count_green += 1
            if self._count_green > 7:
                self._green = True
                self._count_green = 0
                self._count_red = 0
        elif green - red < _RED_GREEN_DIFF_RED_LEVEL:
            self._count_red += 1
        else:
            self._count_no_green += 1
            if self._count_no_green > 7:
                self._green = False
                self._count_green = 0
                self._count_red = 0
        if not self._green:
            if self._count_red > 10:
                return RED
            if green > _WHITE_LEVEL_GREEN:
                return WHITE
            else:
                return BLACK
        else:
            return GREEN
        
    def reset(self):
        self._count_no_green = 0
        self._count_green = 0
        self._count_red = 0
        self._green = False

###### green filter instances ######
green_left = _GreenFilter(green_sensors[0], green_sensors[1], red_sensors[0], red_sensors[1])
green_right = _GreenFilter(green_sensors[3], green_sensors[2], red_sensors[3], red_sensors[2])

###### test functions ######

def test_white():
    while True:
        measure_white()
        print("_raw_white_light")
        time.sleep_ms(500)

def test_adc():
    set_channel(p.ADC_PT_M)
    while True: 
        print(read_raw_adc())
        time.sleep_ms(500)

def test_raw_all():
    while True:
        measure_white()
        measure_green_red()
        print("_raw_white_light: ", end='')
        print([sens.val for sens in all_sensors])
        print("_raw_green_light: ", end='')
        print([sens.val for sens in green_sensors])
        print("_raw_red_light: ", end='')
        print([sens.val for sens in red_sensors])
        time.sleep_ms(200)
