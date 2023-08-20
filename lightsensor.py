import adc_multi
import led
import time
import sensor

_USE_WHITE_LEDS: bool = True
_USE_RGB_WHITE_LEDS: bool = False

###### Level for colors ######
_WHITE_LEVEL: int = 0
_DARK_LEVEL: int = 0
_RED_GREEN_DIFF_GREEN_LEVEL: int = 0
_RED_GREEN_DIFF_RED_LEVEL: int = 0
_WHITE_LEVEL_GREEN: int = 0

###### colors ######
COLOR = int
GREEN:  COLOR = 2
BLACK:  COLOR = 1
WHITE:  COLOR = 0
RED:    COLOR = 3
SILVER: COLOR = 4

###### directions ######
DIRECTION = int
FORWARD:  DIRECTION = 0
LEFT:     DIRECTION = 1
RIGHT:    DIRECTION = -1
BACKWARD: DIRECTION = 3

###### measure functions ######


def measure_white():
    """measuer sensors with white light"""
    if _USE_RGB_WHITE_LEDS:
        led.set_lightsensorbar_rgb(led.WHITE)
    if _USE_WHITE_LEDS:
        led.set_lightsensorbar_white(True)
    for sens in sensor.white:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.OFF)
    led.set_lightsensorbar_white(False)


def measure_green_red() -> list[int]:
    """measure sensors with green and red light"""
    led.set_lightsensorbar_rgb(led.GREEN)
    for sens in sensor.green:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.RED)
    for sens in sensor.red:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.OFF)


###### line follower functions ######

def all_white() -> bool:
    """check if all sensors see white"""
    for sens in sensor.white:
        if sens.map_raw_value() < _WHITE_LEVEL:
            return False
    return True


def outer_see_dark() -> bool:
    """check if outer sensors see non white"""
    return sensor.white[0].val < _DARK_LEVEL or sensor.white[-1] < _DARK_LEVEL


def get_linefollower_diff_raw() -> float:
    """get linefollower diff without mapping to calibration"""
    diff_middle = sensor.white[1].val - sensor.white[3].val
    diff_inside = sensor.white[0].val - sensor.white[4].val
    diff = diff_inside + diff_middle * 2
    return diff // 25


def get_linefollower_diff() -> int:
    """get linefollower diff with mapping to calibration"""
    diff_midddle = (sensor.white[1].map_raw_value() -
                    sensor.white[3].map_raw_value())
    diff_inside = (sensor.white[0].map_raw_value() -
                   sensor.white[4].map_raw_value())
    diff = diff_inside + diff_midddle * 2
    return diff


def decide_crossroad(values: list[list[COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """
    left = values[0]
    right = values[1]
    lg = 0
    rg = 0
    if left[0] == GREEN and left[1] == BLACK:
        lg = 1
    if right[0] == GREEN and right[1] == BLACK:
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
    # really need to clean up this abomination of a class
    def __init__(
            self,
            green_sens: sensor.Sensor,
            red_sens: sensor.Sensor
    ):
        self._green_sens = green_sens
        self._red_sens = red_sens
        self._count_no_green = 0
        self._count_green = 0
        self._green = False
        self._count_red = 0

    def get_color(self) -> COLOR:
        green = self._green_sens.val
        red = self._red_sens.val
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
green_left = _GreenFilter(
    sensor.green[0],
    sensor.red[0],
)
green_right = _GreenFilter(
    sensor.green[1],
    sensor.red[1],
)

###### test functions ######


def test_white():
    """print raw white light values"""
    while True:
        measure_white()
        print([sens.val for sens in sensor.white])
        time.sleep_ms(100)


def test_all():
    """print raw light values for all sensors"""
    while True:
        measure_white()
        measure_green_red()
        print("_raw_white_light: ", end='')
        print([sens.val for sens in sensor.white])
        print("_raw_green_light: ", end='')
        print([sens.val for sens in sensor.green])
        print("_raw_red_light: ", end='')
        print([sens.val for sens in sensor.red])
        time.sleep_ms(100)


def test_red_green():
    """print raw red and green light values + difference"""
    while True:
        measure_green_red()
        print("red: ", end='')
        print([sens.val for sens in sensor.red])
        print("green: ", end='')
        print([sens.val for sens in sensor.green])
        print("diff: ", end='')
        print([sensor.red[i].val - sensor.green[i].val for i in range(2)])
        time.sleep_ms(100)
