import sensor
import led
from adc_multi import set_channel, read_raw_adc

_PRINT_CALIB: bool = True
_SAMPLE_NUMBERS: int = 1200


def write_calib():
    f = open("calib_data.txt", "r")
    for sens in sensor.all:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    for sens in sensor.green:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    for sens in sensor.red:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    f.close()


def read_calib():
    try:
        f = open("calib_data.txt")
        if _PRINT_CALIB:
            print("white sensors:")
        for sens in sensor.all:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
        if _PRINT_CALIB:
            print("green sensors:")
        for sens in sensor.green:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
        if _PRINT_CALIB:
            print("red sensors:")
        for sens in sensor.red:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
    except BaseException:
        pass


def calibrate():
    led.set_lightsensorbar_white(True)
    for sens in sensor.all:
        set_channel(sens.channel)
        for _ in _SAMPLE_NUMBERS:
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    led.set_lightsensorbar_white(False)
    led.set_lightsensorbar_rgb(led.GREEN)
    for sens in sensor.green:
        set_channel(sens.channel)
        for _ in _SAMPLE_NUMBERS:
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    led.set_lightsensorbar_rgb(led.RED)
    for sens in sensor.red:
        set_channel(sens.channel)
        for _ in range(_SAMPLE_NUMBERS):
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    led.set_lightsensorbar_rgb(led.OFF)
