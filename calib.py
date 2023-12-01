import adc_multi
import led
import sensor
import time

_PRINT_CALIB: bool = False
_SAMPLE_NUMBERS: int = 3000

print("calib...........crash")


def write_to_file():
    """write calibration data from sensor instances to calib_data.txt"""
    f = open("calib_data.txt", "w")
    for sens in sensor.white:
        f.write("%d %d\n" % (sens.min, sens.max))
    for sens in sensor.green:
        f.write("%d %d\n" % (sens.min, sens.max))
    for sens in sensor.red:
        f.write("%d %d\n" % (sens.min, sens.max))
    f.close()


def load_from_file():
    """load calibration data from calib_data.txt to sensor instances"""
    try:
        f = open("calib_data.txt")
        for sens in sensor.white:
            value = f.readline().strip().split()
            sens.min, sens.max = [int(val) for val in value]
        for sens in sensor.green:
            value = f.readline().strip().split()
            sens.min, sens.max = [int(val) for val in value]
        for sens in sensor.red:
            value = f.readline().strip().split()
            sens.min, sens.max = [int(val) for val in value]
        if _PRINT_CALIB:
            print("calibration read")
            show()
    except BaseException:
        pass


def _calib(sensors):
    """helper function calibrate sensor list"""
    for sens in sensors:
        sens.min = 4096
        sens.max = 0
    for _ in range(_SAMPLE_NUMBERS):
        for sens in sensors:
            adc_multi.set_channel(sens.channel)
            time.sleep_us(200)
            val = adc_multi.read_raw()
            sens.min = min(sens.min, val)
            sens.max = max(sens.max, val)


def start():
    """do calibration"""
    led.set_lightsensorbar_white(True)
    _calib(sensor.white)
    led.set_lightsensorbar_white(False)
    led.set_lightsensorbar_rgb(led.GREEN)
    _calib(sensor.green)
    led.set_lightsensorbar_rgb(led.RED)
    _calib(sensor.red)
    led.set_lightsensorbar_rgb(led.OFF)
    if _PRINT_CALIB:
        print("calbration done")
        show()


def show():
    """print calibration data from sensor instances"""
    print("white:")
    for sens in sensor.white:
        print(sens.min, sens.max)
    print("green:")
    for sens in sensor.green:
        print(sens.min, sens.max)
    print("red:")
    for sens in sensor.red:
        print(sens.min, sens.max)
