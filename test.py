import lightsensor
import led
import color
import motor
import linefollower
import gyro
import servo
import button
import time
import grappler


def measure_rate():
    start = time.ticks_ms()
    for _ in range(1000):
        lightsensor.measure_green_red()
        lightsensor.measure_white()
        color.get()
    end = time.ticks_ms()
    print(end - start)


def run():
    # lightsensor ##############################
    # lightsensor.test_reflective()
    # lightsensor.test_outer_diff()
    # lightsensor.test_linefollower_diffs_all()
    # lightsensor.test_all()
    # lightsensor.test_white()
    # lightsensor.test_red_green()
    # lightsensor.test_red_green_calib()
    # lightsensor.test_all_calib()
    # lightsensor.test_green_red_diff()
    # lightsensor.test_linefollower_diff()

    # color ####################################
    # color.test()

    # led ######################################
    # led.test_status()
    # led.set_status_left(led.OFF)
    # led.set_status_right(led.OFF)

    # linefollower #############################
    linefollower.test_linefollower()
    # linefollower.test_turn_direction()
    # linefollower.test_crossroad()
    # linefollower.test_turn_angle()

    # gyro #####################################
    # gyro.test()

    # motor ####################################
    # motor.test()
    # motor.test_forward()

    # servo ####################################
    # servo.test(servo.FOUR)
    # servo.test_all()
    # servo.test180()

    # button ###################################
    # button.test()

    # speed ####################################
    # measure_rate()
    pass


if __name__ == "__main__":
    run()
