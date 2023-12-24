import adc_multi
import led
import time
import sensor
import math

# toggle to use the white leds on the bar for measuring white
_USE_WHITE_LEDS: bool = True
# toggle to use the rgb leds on the bar to measure white
_USE_RGB_WHITE_LEDS: bool = False

###### Level for colors ######
_WHITE_LEVEL: int = 0

###### colors ######
COLOR = int
GREEN:  COLOR = 2
BLACK:  COLOR = 1
WHITE:  COLOR = 0
RED:    COLOR = 3
SILVER: COLOR = 4

color_map = {GREEN: "green", RED: "reeed", BLACK: "black", WHITE: "white"}

###### measure functions ######
# dont turn off leds after measure


def measure_white():
    """measure sensors with white light"""
    led.set_lightsensorbar_white(True)
    time.sleep_us(30)
    for sens in sensor.white:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_white(False)
    time.sleep_us(30)


# def measure_white_rgb():
#     """measure sensors with rgb led set to white"""
#     led.set_lightsensorbar_rgb(led.WHITE)
#     for sens in sensor.white:


def measure_green_red():
    """measure sensors with green and red light"""
    led.set_lightsensorbar_rgb(led.GREEN)
    time.sleep_us(10)
    for sens in sensor.green:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.RED)
    time.sleep_us(10)
    for sens in sensor.red:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_rgb(led.OFF)
    time.sleep_us(10)


def measure_reflective():
    led.set_lightsensorbar_white(True)
    time.sleep_us(30)
    for sens in sensor.silver:
        adc_multi.set_channel(sens.channel)
        sens.val = adc_multi.read_raw()
    led.set_lightsensorbar_white(False)
    time.sleep_us(30)


###### line follower functions ######

def all_white() -> bool:
    """check if all sensors see white"""
    for sens in sensor.white:
        if sens.map_raw_value() < _WHITE_LEVEL:
            return False
    return True


def get_linefollower_diff() -> int:
    """get linefollower diff without mapping to calibration"""
    diff_middle = sensor.white[1].val - sensor.white[3].val
    diff_inside = sensor.white[0].val - sensor.white[4].val
    diff = diff_inside + diff_middle * 2
    return diff // 25


def get_linefollower_diff_calib() -> int:
    """get linefollower diff with mapping to calibration"""
    diff_midddle = (sensor.white[1].map_raw_value() -
                    sensor.white[3].map_raw_value())
    diff_outside = (sensor.white[0].map_raw_value() -
                    sensor.white[4].map_raw_value())
    if abs(diff_outside) < 30:
        diff_outside = 0
    diff = math.copysign(
        math.sqrt(abs(float(diff_midddle))),
        diff_midddle)*4 + diff_midddle
    return diff // 2


def get_linefollower_diff_outside() -> int:
    """return calib diff of outer sensors"""
    diff_outside = (sensor.white[0].map_raw_value() -
                    sensor.white[4].map_raw_value())
    return diff_outside


def get_linefollower_diff_test() -> int:
    diff_midddle = (sensor.white[3].map_raw_value() -
                    sensor.white[1].map_raw_value())
    return diff_midddle


def get_green_red_diff() -> int:
    """get difference between green and red"""
    return [
        sensor.green[0].map_raw_value() - sensor.red[0].map_raw_value(),
        sensor.green[1].map_raw_value() - sensor.red[1].map_raw_value()
    ]


def get_green() -> list[int]:
    """get green light values"""
    return [sensor.green[0].map_raw_value(), sensor.green[1].map_raw_value()]


###### test functions ######


def test_white():
    """print raw white light values"""
    while True:
        measure_white()
        print([sens.val for sens in sensor.white])
        time.sleep_ms(100)


def test_reflective():
    while True:
        measure_reflective()
        print([sens.val for sens in sensor.silver])
        time.sleep_ms(100)


def test_all_calib():
    """print calib light values for all sensors"""
    while True:
        measure_white()
        measure_green_red()
        print("white: ", end='')
        print([sens.map_raw_value() for sens in sensor.white])
        print("green: ", end='')
        print([sens.map_raw_value() for sens in sensor.green])
        print("red: ", end='')
        print([sens.map_raw_value() for sens in sensor.red])
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
        print(
            [sensor.red[i].val - sensor.green[i].val for i in range(2)]
        )
        time.sleep_ms(100)


def test_green_red_diff():
    """print mapped red and green light values + difference"""
    while True:
        measure_green_red()
        print("red: ", end='')
        print([sens.map_raw_value() for sens in sensor.red])
        print("green: ", end='')
        print([sens.map_raw_value() for sens in sensor.green])
        print("diff: ", end='')
        print(get_green_red_diff())
        time.sleep_ms(100)


def test_linefollower_diffs_all():
    """komisch"""
    while True:
        measure_white()
        diff_middle = sensor.white[1].val - sensor.white[3].val
        diff_left = sensor.white[1].val - sensor.white[2].val
        diff_right = sensor.white[3].val - sensor.white[2].val
        print("middle: ", diff_middle)
        print("left: ", diff_left)
        print("right: ", diff_right)
        time.sleep_ms(200)


def test_outer_diff():
    """print diff of outer white sensors"""
    while True:
        measure_white()
        print(get_linefollower_diff_outside())
        time.sleep_ms(200)


def test_linefollower_diff():
    """print calib diff for linefollower"""
    while True:
        measure_white()
        print("calib: ", get_linefollower_diff_calib())
        print("normal ", get_linefollower_diff())
        time.sleep_ms(100)
