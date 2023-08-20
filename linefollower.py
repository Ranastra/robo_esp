import motor
import lightsensor
import time


base_v = 50
print("HELP")


def test_linefollower():
    while True:
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff()
        # print(diff)
        motor.drive(motor.MOT_A, base_v + diff)
        motor.drive(motor.MOT_B, base_v - diff)
        # time.sleep_ms(100)


test_linefollower()
# lightsensor.test_white()
# lightsensor.test_white()
