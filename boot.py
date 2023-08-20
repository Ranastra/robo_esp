import calib
import led
import motor
import sys

print("in boot.py... where are my boots?")

# clear cache
sys.modules.clear()

# motor off
motor.stop(motor.MOT_AB)

# LEDs off
led.set_status_left(led.OFF)
led.set_status_right(led.OFF)
led.set_lightsensorbar_rgb(led.OFF)
led.set_lightsensorbar_white(False)

# read sensor calib
calib.load_from_file()
