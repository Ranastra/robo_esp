import motor
import utime
import lightsensor
import color
import led
import gyro
import button
import sensor

# this module will host helper functions for the linefollower
# combining sensors, motor and decision making

###### directions ######
DIRECTION = int
FORWARD:  DIRECTION = 0
LEFT:     DIRECTION = 1
RIGHT:    DIRECTION = -1
BACKWARD: DIRECTION = 3

# map direction constants to names
direction_map = {FORWARD: "forward", LEFT: "left",
                 RIGHT: "right", BACKWARD: "backward"}

V0: int = 70

# flags
CHECK_FOR_HOVER: bool = True

ON_RAMP_UP: int = 0
ON_RAMP_DOWN: int = 1
FLAT_BORING: int = 2
RAMP_MAP = {ON_RAMP_DOWN: 'ON_RAMP_DOWN', ON_RAMP_UP: 'ON_RAMP_UP', FLAT_BORING: 'FLAT_BORING'}


def decide_crossroad(values: list[list[lightsensor.COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """  # TODO
    (left, right, first, second) = (0, 1, 0, 1)
    if values[left][first] == lightsensor.GREEN and values[right][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.BLACK or values[right][second] == lightsensor.BLACK:
            return BACKWARD
        else:
            return FORWARD
    elif values[left][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.WHITE:
            return FORWARD
        else:
            return LEFT
    else:
        if values[right][second] == lightsensor.WHITE:
            return FORWARD
        else:
            return RIGHT


def watch_hover():
    """check if the robot is hovered in the air"""
    if CHECK_FOR_HOVER and lightsensor.is_hovered():
        motor.stop(motor.MOT_AB)
        while lightsensor.is_hovered():
            lightsensor.measure_white()


def until_green_end(direction: DIRECTION) -> list[int]:
    """
    dont change driving until the other side sees green,
    than returns the current colors
    """
    while True:
        lightsensor.measure_green_red()
        values = color.get()
        if (
                (direction == LEFT and values[0] != lightsensor.GREEN) or
                (direction == RIGHT and values[1] != lightsensor.GREEN)
        ):
            # print(values)
            # utime.sleep_ms(50)
            # values = color.get()
            return values


def drive_off_green(direction: DIRECTION) -> list[list[lightsensor.COLOR]]:
    """
    gets called after one sensor sees green, drive until green ends on this side
    measure, on the other side, and store which color comes after green
    return the colors as [left[first, second], right[first, second]]
    """
    motor.drive(motor.MOT_AB, V0)
    values = [
        [lightsensor.WHITE, lightsensor.WHITE],
        [lightsensor.WHITE, lightsensor.WHITE]
    ]
    (left, right) = (0, 1)
    if direction == LEFT:
        values[left][0] = lightsensor.GREEN
    else:
        values[right][0] = lightsensor.GREEN
    motor.drive(motor.MOT_AB, V0)
    while True:
        lightsensor.measure_green_red()
        (color_left, color_right) = color.get()
        if direction == LEFT:
            if color_right == lightsensor.GREEN:
                values[right][0] = color_right
            if color_left != lightsensor.GREEN:
                utime.sleep_ms(100)
                (color_left, color_right) = color.get()
                values[left][1] = color_left
                values[right][1] = until_green_end(RIGHT)[right]
                break
        else:
            if color_left == lightsensor.GREEN:
                values[left][0] = color_left
            if color_right != lightsensor.GREEN:
                utime.sleep_ms(100)
                (color_left, color_right) = color.get()
                values[right][1] = color_right
                values[left][1] = until_green_end(LEFT)[left]
                break
    motor.stop(motor.MOT_AB)
    return values


def drive_angle(angle: float):
    """drive angle with gyro"""
    V0 = 100
    gyro.reset()
    if angle > 0:
        motor.drive(motor.MOT_A, V0)
        motor.drive(motor.MOT_B, -V0)
        while gyro.angle[2] < angle:
            gyro.update()
    else:
        motor.drive(motor.MOT_B, V0)
        motor.drive(motor.MOT_A, -V0)
        while gyro.angle[2] > angle:
            gyro.update()
    motor.stop(motor.MOT_AB)


def turn_direction(direction: DIRECTION):
    """turn direction at crossroad with some corrections"""
    # TODO verschiedene Geschwindikeiten oder stottern
    V0 = 70
    # try correcting with gyro # TODO
    # drive_angle(-gyro.angle[2])  # this will prob break everything
    # drive a bit forward
    if direction == BACKWARD:
        motor.drive(motor.MOT_AB, V0)
        utime.sleep_ms(150)
    gyro.reset()
    if direction == LEFT:
        drive_angle(-80.0)
    elif direction == RIGHT:
        drive_angle(80.0)
    elif direction == BACKWARD:
        drive_angle(180.0)
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(300)
    motor.stop(motor.MOT_AB)


def run():
    test_linefollower()


def test_linefollower(basic_time_end=0):
    """linefollower"""
    V0 = 55
    V0_OFF = 20 # V0 base v for faster side and v for slower side = V0 - V0_OFF
    if basic_time_end == 0:
        basic_time_end, basic_flag = utime.ticks_ms(), False
    else:
        basic_flag = True
    while True:
        # normal linefollowing
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff_calib()
        diff_outer = lightsensor.get_linefollower_diff_outside()
        ramp_mode = on_ramp()
        mode_line = 0
        if basic_flag:
            v = 35
            mode_line = 1
        else:
            if ramp_mode == ON_RAMP_UP:
                diff //= 3
                diff_outer //= 3
                v = 100
                mode_line = 1
            elif ramp_mode == ON_RAMP_DOWN:
                diff //= 7
                diff_outer //= 7
                v = V0 - 30
                mode_line = 1
            else:
                v = V0
                model_line = 0
        # if abs(diff_outer) > 70 and not basic_flag:
        if False:
            if diff_outer < 0:
                vr = 100
                vl = -40
            else:
                vl = 100
                vr = -40
        else:
            # if abs(diff) == 0:
            #     scaler = 1.5
            # else:
            #     scaler = min(max((abs(diff) + 3) / abs(diff) - 1, 0.0), 1.5)
            if mode_line == 1:
                if diff < 0:
                    # vr = (v + abs(diff) * 3) + abs(diff_outer)
                    # vl = (v - abs(diff) * 3 - V0_OFF) - abs(diff_outer) 
                    # vr = int((v + abs(diff) * 3) * scaler) + abs(diff_outer)
                    # vl = int((v - abs(diff) * 3 - V0_OFF) * scaler) - abs(diff_outer) 
                    vr = v + abs(diff) * 1 + abs(diff_outer) * 2
                    vl = v - abs(diff) * 1 - abs(diff_outer) * 2
                else:
                    # vl = int((v + abs(diff) * 3) * scaler) + abs(diff_outer)
                    # vr = int((v - abs(diff) * 3 - V0_OFF) * scaler) - abs(diff_outer) 
                    vl = v + abs(diff) * 1 + abs(diff_outer) * 2
                    vr = v - abs(diff) * 1 - abs(diff_outer) * 2
            else:

        print(vl, vr)
        motor.drive(motor.MOT_A, vl)
        motor.drive(motor.MOT_B, vr)
        # check for negative light values
        # watch_hover()
        # check for events
        if not basic_flag:
            # if True:
            for _ in range(2):
                lightsensor.measure_green_red()
                (color_l, color_r) = color.get()
            lightsensor.measure_reflective()
            if color_l == lightsensor.GREEN or color_r == lightsensor.GREEN:
                print("greeeen")
                # check for green
                if color_l == lightsensor.GREEN:
                    vals = drive_off_green(LEFT)
                else:
                    vals = drive_off_green(RIGHT)
                direction = decide_crossroad(vals)
                print(vals)
                print([[lightsensor.color_map[color]
                      for color in pair]for pair in vals])
                print(direction_map[direction])
                utime.sleep_ms(1000)
                turn_direction(direction)
                basic_time_end, basic_flag = utime.ticks_ms() + 700, True
                # v_basic_shadow = 35
            elif color_l == lightsensor.RED or color_r == lightsensor.RED:
                # check for red
                print("reeed")
                motor.stop(motor.MOT_AB)
                utime.sleep_ms(10_000)
            elif lightsensor.on_silver() and ramp_mode == FLAT_BORING:
                print("silveeeer")
                # check for reflective
                motor.stop(motor.MOT_AB)
                led.set_status_locked(2, led.WHITE)
                utime.sleep_ms(1000)
                return
            elif not button.left.value() or not button.right.value():
                print("button")
                motor.stop(motor.MOT_AB)
                utime.sleep_ms(300)
                # check for collisions
                if not button.left.value() or not button.right.value():
                    drive_around_object(LEFT)
                basic_time_end, basic_flag = utime.ticks_ms() + 600, True
            # TODO try correcting with gyro
            # if lightsensor.inner_see_dark():
            #     gyro.active_update()
        else:
            basic_flag = utime.ticks_ms() < basic_time_end
            # if not basic_flag:
            #     v_basic_shadow = V0


def drive_around_object(direction: DIRECTION):
    """drive around an object after collision"""
    V0 = 82
    motor.drive(motor.MOT_AB, -60)
    led.set_status_locked(2, led.CYAN)
    utime.sleep_ms(150)
    vdiff = 65
    drive_angle(-70.0*direction)
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(100)
    motor.drive(motor.MOT_A, V0 + vdiff*direction)
    motor.drive(motor.MOT_B, V0 - vdiff*direction)
    lightsensor.measure_white()
    start = utime.ticks_ms()
    while True:
        if not lightsensor.all_white() and utime.ticks_ms() - start > 500:
            break
        lightsensor.measure_white()
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(150)
    drive_angle(-60.0*direction)


def on_ramp():
    val = gyro.get_tilt()
    if val > 0.15:
        return ON_RAMP_DOWN
    elif val < -0.1:
        return ON_RAMP_UP
    else:
        return FLAT_BORING


def test_crossroad():
    """test for green detection at crossroads, prints the colors"""
    motor.drive(motor.MOT_AB, V0)
    while True:
        lightsensor.measure_white()
        lightsensor.measure_green_red()
        diff = lightsensor.get_linefollower_diff_calib()
        motor.drive(motor.MOT_A, V0 + diff)
        motor.drive(motor.MOT_B, V0 - diff)
        colors = color.get()
        if colors[0] == lightsensor.GREEN:
            print("left")
            print([[[lightsensor.color_map[val] for val in direc]
                  for direc in drive_off_green(LEFT)]])
            break
        elif colors[1] == lightsensor.GREEN:
            print("right")
            # print(drive_off_green(RIGHT))
            print([[[lightsensor.color_map[val] for val in direc]
                  for direc in drive_off_green(RIGHT)]])
            break


def test_turn_direction():
    """unit test for turn_direction"""
    gyro.calib()
    for _ in range(2):
        print("left")
        turn_direction(LEFT)
        utime.sleep(1)
        print("right")
        turn_direction(RIGHT)
        utime.sleep(1)
        print("forward")
        turn_direction(FORWARD)
        utime.sleep(1)
        print("backward")
        turn_direction(BACKWARD)
        utime.sleep(1)


def test_watch_hover():
    while True:
        print("watching")
        lightsensor.measure_white()
        for sens in sensor.white:
            print(sens.map_raw_value(), end=" ")
        print()
        watch_hover()
        print("end")
        utime.sleep_ms(300)


def test_turn_angle():
    """unit test for turn_direction"""
    gyro.calib()
    while True:
        print("left")
        drive_angle(-90.0)
        utime.sleep(1)
        print("right")
        drive_angle(90.0)
        utime.sleep(1)


def test_drive_forward_gyro():
    """drive forward with gyro"""
    gyro.calib()
    gyro.reset()
    while True:
        gyro.update()
        print(gyro.angle[0])

def test_ramp():
    while True:
        utime.sleep_ms(500)
        print(RAMP_MAP[on_ramp()])


if __name__ == "__main__":
    run()
