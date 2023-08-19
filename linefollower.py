import motor
import lightsensor


base_v = 50
print("HELP")


def test_linefollower():
    while True:
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff()
        motor.drive(motor.MOT_A, base_v + diff)
        motor.drive(motor.MOT_B, base_v - diff)
