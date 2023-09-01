import led
import calib
import motor
import lightsensor
import time

calib.start()
calib.show()
time.sleep(10)
base_v = 50


def test_linefollower():
    while True:
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff_calib()
        # print(diff)
        motor.drive(motor.MOT_A, base_v + diff)
        motor.drive(motor.MOT_B, base_v - diff)
        # time.sleep_ms(100)


lightsensor.test_red_green_calib()

# test_linefollower()
# lightsensor.test_white()
# lightsensor.test_white()
# led.set_status_left(led.RED)
# calib.start()
# calib.load_from_file()
# calib.show()
# calib.write_to_file()
# led.set_status_left(led.GREEN)
# lightsensor.test_red_green()

# test_linefollower()
