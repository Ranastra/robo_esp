import lightsensor
import led
import color
import motor
import linefollower
import gyro
import servo
import button
import utime
import grappler
import reset
import i2c
import tof
import calib
import escape_room
import escape_use


def measure_rate():
    start = utime.ticks_ms()
    for _ in range(1000):
        lightsensor.measure_green_red()
        lightsensor.measure_white()
        color.get()
    end = utime.ticks_ms()
    print(end - start)


def run():
    calib.load_from_file()
    calib.show()
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
    # lightsensor.test_front_raw()

    # color ####################################
    # color.test()
    # color.test_front()

    # led ######################################
    # led.test_status()
    # led.set_status_left(led.OFF)
    # led.set_status_right(led.OFF)

    # linefollower #############################
    # linefollower.test_linefollower()
    # linefollower.test_turn_direction()
    # linefollower.test_crossroad()
    # linefollower.test_turn_angle()
    # linefollower.drive_around_object(linefollower.LEFT)
    # linefollower.test_watch_hover()
    # linefollower.test_drive_forward_gyro()
    # linefollower.test_ramp()

    # gyro #####################################
    # gyro.test()
    gyro.test_accell_gyro()

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

    # grappler
    # grappler.down()

    # i2c ######################################
    # i2c.test()

    # tof ######################################
    # tof.test(tof.FOUR)
    # tof.test_two_three()
    # tof.time_one()

    # escape ###################################
    # escape_room.wall_follower()
    # escape_room.find_line(2)
    # escape_room.test_find_line2()

    # escape_use
    # escape_use.run()
    # escape_use.drop_ball(escape_use.BALL_ALIVE)
    pass


# TODO: gyro calibrierung an use case anpassen
# motoren drehen mit


if __name__ == "__main__":
    reset.reset_hardware()
    run()
