import reset
import calib
import rotary_encoder
import utime
import linefollower
import led
import escape_room
import escape_use
import gyro
import test
import motor

print("main.py like maintenance")


def start():
    """setup"""
    # load stored calib
    calib.load_from_file()
    # calibration of gyro
    gyro.calib()
    # got_calibrated_flag = False
    while not rotary_encoder.watch_button_press(): #TODO: write on the robot
    # while rotary_encoder.watch_button_press():
        led.set_status_locked(2, led.PURPLE)
        val = rotary_encoder.watch_rotary()
        if val == 1:
            # calibrate lightsensors
            led.set_status_locked(2, led.RED)
            utime.sleep_ms(500)
            # if got_calibrated_flag: not gonna do this
            #     calib.calib_front()
            #     got_calibrated_flag = False
            # else:
            calib.start()
            # got_calibrated_flag = True
            calib.write_to_file()
        if val == -1:
            # run tests
            led.set_status_locked(2, led.BLUE)
            utime.sleep_ms(500)
            test.run()
    led.set_status_locked(2, led.GREEN)
    utime.sleep_ms(500)


def run():
    led.set_status_locked(2, led.PURPLE)
    utime.sleep_ms(500)
    linefollower.run()
    led.set_status_locked(2, led.BLUE)
    utime.sleep_ms(500)
    escape_use.run()
    escape_room.run(skip=True) # drive out of this hell
    led.set_status_locked(2, led.PURPLE)
    utime.sleep_ms(500)
    linefollower.run()


def stop():
    """cleanup"""
    reset.run()


while True:
    # try:
    #     reset.reset_hardware()
    #     start()
    #     run()
    #     stop()
    # except:
    #     motor.stop(motor.MOT_AB)
    #     led.set_status_locked(2, led.GREEN)
    #     utime.sleep_ms(500)
    reset.reset_hardware()
    start()
    run()
    stop()
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.GREEN)
    utime.sleep_ms(500)
