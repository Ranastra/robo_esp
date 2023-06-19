from sensor import all_sensors, green_sensors, red_sensors
from led import set_lightsensorbar_white, set_lightsensorbar_led, GREEN, RED, OFF
from adc_multi import set_channel, read_raw_adc

_PRINT_CALIB:bool = const(True)
_SAMPLE_NUMBERS:int = const(1200)


def write_calib():
    f = open("calib_data.txt", "r")
    for sens in all_sensors:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    for sens in green_sensors:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    for sens in red_sensors:
        f.write("%d %d\n" % (sens.min_val, sens.max_val))
    f.close()

def read_calib():
    try:
        f = open("calib_data.txt")
        if _PRINT_CALIB:
            print("white sensors:")
        for sens in all_sensors:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
        if _PRINT_CALIB:
            print("green sensors:")
        for sens in green_sensors:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
        if _PRINT_CALIB:
            print("red sensors:")
        for sens in red_sensors:
            value = f.readline().strip().split()
            if _PRINT_CALIB:
                print(sens.channel, value)
            sens.min_val, sens.max_val = [int(val) for val in value]
    except BaseException:
        pass


def calibrate():
    set_lightsensorbar_white(True)
    for sens in all_sensors:
        set_channel(sens.channel)
        for _ in _SAMPLE_NUMBERS:
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    set_lightsensorbar_white(False)
    set_lightsensorbar_led(GREEN)
    for sens in green_sensors:
        set_channel(sens.channel)
        for _ in _SAMPLE_NUMBERS:
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    set_lightsensorbar_led(RED)
    for sens in red_sensors:
        set_channel(sens.channel)
        for _ in range(_SAMPLE_NUMBERS):
            val = read_raw_adc()
            if val < sens.min_val:
                sens.min_val = val
            elif val > sens.max_val:
                sens.max_val = val
    set_lightsensorbar_led(OFF)