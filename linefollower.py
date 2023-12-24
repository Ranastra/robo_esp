import motor
import sensor
import time
import calib
import lightsensor
import color
import led
import gyro
# import time

# this module will host helper functions for the linefollower
# combining sensors, motor and decision making

###### directions ######
DIRECTION = int
FORWARD:  DIRECTION = 0
LEFT:     DIRECTION = 1
RIGHT:    DIRECTION = -1
BACKWARD: DIRECTION = 3

direction_map = {FORWARD: "forward", LEFT: "left",
                 RIGHT: "right", BACKWARD: "backward"}

V0: int = 50


def decide_crossroad(values: list[list[lightsensor.COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """
    # (left, right, first, second) = (0, 1, 0, 1)
    # left_green_black = (
    #     values[left][first] == lightsensor.GREEN and
    #     values[left][second] == lightsensor.BLACK
    # )
    # right_green_black = (
    #     values[right][first] == lightsensor.GREEN and
    #     values[right][second] == lightsensor.BLACK
    # )
    # if left_green_black and right_green_black:
    #     return BACKWARD
    # elif left_green_black:
    #     return LEFT
    # elif right_green_black:
    #     return RIGHT
    # else:
    #     return FORWARD
    (left, right, first, second) = (0, 1, 0, 1)
    if values[left][first] == lightsensor.GREEN and values[right][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.BLACK and values[right][second] == lightsensor.BLACK:
            return BACKWARD
        else:
            return FORWARD
    elif values[left][first] == lightsensor.GREEN:
        return LEFT
    else:
        return RIGHT


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
            return values

###### tests ######


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
    left, right = 0, 1
    if direction == LEFT:
        values[left][0] = lightsensor.GREEN
    else:
        values[right][0] = lightsensor.GREEN
    motor.drive(motor.MOT_AB, V0)
    while True:
        lightsensor.measure_green_red()
        colors = color.get()
        if direction == RIGHT:
            if colors[left] != lightsensor.GREEN:
                values[left][1] = colors[left]
                values[right][1] = until_green_end(RIGHT)[right]
                break
            elif colors[right] == lightsensor.GREEN:
                values[right][0] = lightsensor.GREEN
        if direction == LEFT:
            if colors[right] != lightsensor.GREEN:
                values[right][1] = colors[right]
                values[left][1] = until_green_end(LEFT)[left]
                break
            elif colors[left] == lightsensor.GREEN:
                values[left][0] = lightsensor.GREEN
    motor.stop(motor.MOT_AB)
    return values


def turn_direction(direction: DIRECTION):
    motor.stop(motor.MOT_AB)
    gyro.reset()
    if direction == LEFT:
        motor.drive(motor.MOT_B, V0)
        motor.drive(motor.MOT_A, -V0)
        while gyro.angle[2] > -90.0:
            gyro.update()
    elif direction == FORWARD:
        pass
    else:
        motor.drive(motor.MOT_A, V0)
        motor.drive(motor.MOT_B, -V0)
        if direction == RIGHT:
            while gyro.angle[2] < 90.0:
                gyro.update()
        else:
            while gyro.angle[2] < 180.0:
                gyro.update()
    motor.drive(motor.MOT_AB, V0)
    time.sleep(1)
    motor.stop(motor.MOT_AB)


def linefollower():
    while True:
        lightsensor.measure_white()
        lightsensor.measure_green_red()
        diff = lightsensor.get_linefollower_diff_calib()
        motor.drive(motor.MOT_A, V0 + diff)
        motor.drive(motor.MOT_B, V0 - diff)
        colors = color.get()
        if colors[0] == lightsensor.GREEN:
            print("left green")
            vals = drive_off_green(LEFT)
            print(vals)
            direc = decide_crossroad(vals)
            print(direc)
            break
        if colors[1] == lightsensor.GREEN:
            print("right green")
            vals = drive_off_green(RIGHT)
            print(vals)
            direc = decide_crossroad(vals)
            print(direc)
            break


def test_linefollower():
    faktor = 3
    base_v = 100
    while True:
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff_calib()
        diff_outer = lightsensor.get_linefollower_diff_outside()
        # if abs(diff_outer) > 70:
        if abs(diff_outer) > 70:
            if diff_outer < 0:
                vr = base_v + abs(diff_outer)
                vl = base_v - abs(diff_outer) * faktor
            else:
                vl = base_v + abs(diff_outer)
                vr = base_v - abs(diff_outer) * faktor
        else:
            if diff < 0:
                vr = base_v + abs(diff) * faktor
                vl = base_v - abs(diff) * faktor
            else:
                vl = base_v + abs(diff) * faktor
                vr = base_v - abs(diff) * faktor
        # vl = max(0, vl)
        # vr = max(0, vr)
        motor.drive(motor.MOT_A, vl)
        motor.drive(motor.MOT_B, vr)


def test_linefollower2():
    # mit led in der mitte + sensor außen, blau umlöten, mittleres paar leds + mittlere sensoren
    base_v = 60
    while True:
        lightsensor.measure_white()
        # lightsensor.measure_green_red()
        # diff_midddle = (sensor.green[1].map_raw_value() -
        #                 sensor.green[0].map_raw_value())
        diff = lightsensor.get_linefollower_diff_test()
        motor.drive(motor.MOT_A, base_v - diff)
        motor.drive(motor.MOT_B, base_v + diff)


def test_direction():
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
