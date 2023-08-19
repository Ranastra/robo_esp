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
GREEN: COLOR = 2
BLACK: COLOR = 1
WHITE: COLOR = 0
RED: COLOR = 3
SILVER: COLOR = 4

###### directions ######
DIRECTION = int
FORWARD: DIRECTION = 0
LEFT: DIRECTION = 1
RIGHT: DIRECTION = -1
BACKWARD: DIRECTION = 3

###### measure functions ######


def measure_white():
    if _USE_RGB_WHITE_LEDS:
        led.set_lightsensorbar_rgb(led.WHITE)
    if _USE_WHITE_LEDS:
        led.set_lightsensorbar_white(True)
    for sens in sensor.all:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.OFF)
    led.set_lightsensorbar_white(False)


def measure_green_red() -> list[int]:
    led.set_lightsensorbar_led(led.GREEN)
    for sens in sensor.green:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_led(led.RED)
    for sens in sensor.red:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_led(led.OFF)


###### line follower functions ######

def all_white() -> bool:
    for sens in sensor.all:
        if sens.map_raw_value() < _WHITE_LEVEL:
            return False
    return True


def outer_see_dark() -> bool:
    return sensor.all[0].val < _DARK_LEVEL or sensor.all[-1] < _DARK_LEVEL


def get_linefollower_diff() -> float:
    # diff_outside = sensor.all[0].val - sensor.all[6].val
    # diff_middle = sensor.all[1].val - sensor.all[5].val
    diff_inside = sensor.all[2].val - sensor.all[4].val
    diff = diff_inside  # + diff_middle * 1.5 + diff_outside * 2  # needs finetuning
    return diff // 40


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
    def __init__(
            self,
            outer_sens_green: sensor.Sensor,
            inner_sens_green: sensor.Sensor,
            outer_sens_red: sensor.Sensor,
            inner_sens_red: sensor.Sensor
    ):
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
green_left = _GreenFilter(
    sensor.green[0], sensor.green[1], sensor.red[0], sensor.red[1])
green_right = _GreenFilter(
    sensor.green[3], sensor.green[2], sensor.red[3], sensor.red[2])

###### test functions ######


def test_white():
    while True:
        measure_white()
        # print("_raw_white_light")
        print([sens.val for sens in sensor.all])
        time.sleep_ms(100)


def test_all():
    while True:
        measure_white()
        measure_green_red()
        print("_raw_white_light: ", end='')
        print([sens.val for sens in sensor.all])
        print("_raw_green_light: ", end='')
        print([sens.val for sens in sensor.green])
        print("_raw_red_light: ", end='')
        print([sens.val for sens in sensor.red])
        time.sleep_ms(100)


def test_red_green():
    while True:
        measure_green_red()
        print("red: ", end='')
        print([sens.val for sens in sensor.red])
        print("green: ", end='')
        print([sens.val for sens in sensor.green])
        print("red - green: ", end='')
        print([sensor.red[i].val - sensor.green[i].val for i in range(4)])
        time.sleep_ms(100)
