import motor
import time
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

V0: int = 50

# flags
CHECK_FOR_HOVER: bool = True


def decide_crossroad(values: list[list[lightsensor.COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """  # TODO
    (left, right, first, second) = (0, 1, 0, 1)
    if values[left][first] == lightsensor.GREEN and values[right][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.BLACK and values[right][second] == lightsensor.BLACK:
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
            # time.sleep_ms(50)
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
                values[left][1] = color_left
                values[right][1] = until_green_end(RIGHT)[right]
                break
        else:
            if color_left == lightsensor.GREEN:
                values[left][0] = color_left
            if color_right != lightsensor.GREEN:
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
    if direction != BACKWARD:
        motor.drive(motor.MOT_AB, V0)
        time.sleep_ms(200)
    gyro.reset()
    if direction == LEFT:
        drive_angle(-70.0)
    elif direction == RIGHT:
        drive_angle(70.0)
    elif direction == BACKWARD:
        drive_angle(180.0)
    motor.drive(motor.MOT_AB, V0)
    time.sleep_ms(100)
    motor.stop(motor.MOT_AB)


def run():
    test_linefollower()


def test_linefollower(basic_time_end=0):
    """linefollower"""
    faktor = 3
    V0 = 50
    v = V0
    if basic_time_end == 0:
        basic_time_end, basic_flag = time.ticks_ms(), False
    else:
        basic_flag = True
    while True:
        # normal linefollowing
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff_calib()
        diff_outer = lightsensor.get_linefollower_diff_outside()
        if abs(diff_outer) > 70:
            if diff_outer < 0:
                vr = v + abs(diff_outer)
                vl = v - abs(diff_outer) * faktor
            else:
                vl = v + abs(diff_outer)
                vr = v - abs(diff_outer) * faktor
        else:
            if diff < 0:
                vr = v + abs(diff) * faktor
                vl = v - abs(diff) * faktor
            else:
                vl = v + abs(diff) * faktor
                vr = v - abs(diff) * faktor
        motor.drive(motor.MOT_A, vl)
        motor.drive(motor.MOT_B, vr)
        # check for negative light values
        # watch_hover()
        # check for events
        if not basic_flag:
            # if True:
            for _ in range(5):
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
                print(direction_map[direction])
                time.sleep_ms(1000)
                turn_direction(direction)
                basic_time_end, basic_flag = time.ticks_ms() + 700, True
                v = 25
            elif color_l == lightsensor.RED or color_r == lightsensor.RED:
                # check for red
                print("reeed")
                motor.stop(motor.MOT_AB)
                time.sleep_ms(10_000)
            elif lightsensor.on_silver():
                print("silveeeer")
                # check for reflective
                motor.stop(motor.MOT_AB)
                led.set_status_locked(2, led.WHITE)
                time.sleep_ms(1000)
                return
            elif not button.left.value() or not button.right.value():
                print("button")
                # check for collisions
                drive_around_object(LEFT)
                basic_time_end, basic_flag = time.ticks_ms() + 600, True
            # TODO try correcting with gyro
            # if lightsensor.inner_see_dark():
            #     gyro.active_update()
        else:
            basic_flag = time.ticks_ms() < basic_time_end
            if not basic_flag:
                v = V0


def drive_around_object(direction: DIRECTION):
    """drive around an object after collision"""
    V0 = 85
    motor.drive(motor.MOT_AB, -60)
    led.set_status_locked(2, led.CYAN)
    time.sleep_ms(200)
    vdiff = 65
    drive_angle(-70.0*direction)
    motor.drive(motor.MOT_AB, V0)
    time.sleep_ms(100)
    motor.drive(motor.MOT_A, V0 + vdiff*direction)
    motor.drive(motor.MOT_B, V0 - vdiff*direction)
    lightsensor.measure_white()
    start = time.ticks_ms()
    while True:
        if not lightsensor.all_white() and time.ticks_ms() - start > 500:
            break
        lightsensor.measure_white()
    motor.drive(motor.MOT_AB, V0)
    time.sleep_ms(250)
    drive_angle(-70.0*direction)


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
        time.sleep(1)
        print("right")
        turn_direction(RIGHT)
        time.sleep(1)
        print("forward")
        turn_direction(FORWARD)
        time.sleep(1)
        print("backward")
        turn_direction(BACKWARD)
        time.sleep(1)


def test_watch_hover():
    while True:
        print("watching")
        lightsensor.measure_white()
        for sens in sensor.white:
            print(sens.map_raw_value(), end=" ")
        print()
        watch_hover()
        print("end")
        time.sleep_ms(300)


def test_turn_angle():
    """unit test for turn_direction"""
    gyro.calib()
    while True:
        print("left")
        drive_angle(-90.0)
        time.sleep(1)
        print("right")
        drive_angle(90.0)
        time.sleep(1)


def test_drive_forward_gyro():
    """drive forward with gyro"""
    gyro.calib()
    gyro.reset()
    while True:
        gyro.update()
        print(gyro.angle[0])


if __name__ == "__main__":
    run()
