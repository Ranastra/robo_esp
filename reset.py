def reset_hardware():
    # motor off
    import motor
    motor.stop(motor.MOT_AB)

    # led off
    import led
    led.set_status_left(led.OFF)
    led.set_status_right(led.OFF)
    led.set_lightsensorbar_rgb(led.OFF)
    led.set_lightsensorbar_white(False)

    # grappler to starting position
    import grappler
    grappler.up()
    grappler.grab()

    # servo off
    import servo
    servo.off(servo.ONE)
    servo.off(servo.TWO)
    servo.off(servo.THREE)
    servo.off(servo.FOUR)


def clear_modules():
    import sys
    # clear modules
    imported_modules = [
        'adc_multi', 'blue', 'boot', 'button', 'calib', 'color', 'grappler',
        'gyro', 'i2c', 'imu', 'led', 'lightsensor', 'linefollower', 'main',
        'micropython_test', 'motor', 'pinesp32', 'vector3d', 'rotary_encoder',
        'sensor', 'servo', 'shift_register', 'ssd1306', 'test'
    ]
    for module in imported_modules:
        if module in sys.modules:
            del sys.modules[module]
    # print("\n".join(sys.modules.keys()))


def run():
    reset_hardware()
    clear_modules()
