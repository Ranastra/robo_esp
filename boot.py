# import clear
import calib
import led
import motor

print("in boot.py... where are my boots?")


# motor off
motor.stop(motor.MOT_AB)

# LEDs off
led.set_status_left(led.YELLOW)
led.set_status_right(led.YELLOW)
led.set_lightsensorbar_rgb(led.OFF)
led.set_lightsensorbar_white(False)

# read sensor calib
calib.load_from_file()
