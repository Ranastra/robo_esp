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
    for sensor_collection in sensor.all:
        for sens in sensor_collection:
            f.write("%d %d\n" % (sens.min, sens.max))
    f.close()


def load_from_file():
    """load calibration data from calib_data.txt to sensor instances"""
    try:
        f = open("calib_data.txt")
        for sensor_collection in sensor.all:
            for sens in sensor_collection:
                value = f.readline().strip().split()
                sens.min, sens.max = [int(val) for val in value]
        f.close()
        if _PRINT_CALIB:
            print("calibration read")
            show()
    except BaseException:
        print("failed to read calibration from file")


def _calib(sensors: list[sensor.Sensor]):
    """helper function calibrate sensor list"""
    for sens in sensors:
        sens.min = 4096
        sens.max = 1
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
    time.sleep_us(20)
    _calib(sensor.white)
    led.set_lightsensorbar_white(False)
    led.set_lightsensorbar_rgb(led.GREEN)
    time.sleep_us(20)
    _calib(sensor.green)
    led.set_lightsensorbar_rgb(led.RED)
    time.sleep_us(20)
    _calib(sensor.red)
    led.set_lightsensorbar_rgb(led.OFF)
    led.set_lightsensorbar_white(True)
    time.sleep_us(20)
    _calib(sensor.silver)
    led.set_lightsensorbar_white(False)
    time.sleep_us(20)
    if _PRINT_CALIB:
        print("calbration done")
        show()


def calib_front():
    """just dont use that"""
    led.set_lightsensorbar_rgb(led.RED)
    time.sleep_us(20)
    _calib(sensor.front_red)
    led.set_lightsensorbar_rgb(led.GREEN)
    time.sleep_us(20)
    _calib(sensor.front_green)
    led.set_lightsensorbar_rgb(led.OFF)
    if _PRINT_CALIB:
        print("calibration done")


def show():
    """print calibration data from sensor instances"""
    for i in range(len(sensor.all)):
        print(sensor.all_names[i])
        for sens in sensor.all[i]:
            print(sens.min, sens.max)
