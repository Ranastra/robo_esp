import time
import lightsensor
import led
import grappler
import color
import gyro
import pinesp32


def run():
    pass


# plan lol
SURVIVOR = True
DEAD = False


def read_from_file() -> int:
    # use some config file to save the number of balls picked up
    # else return 3
    # the file should be resetted every time the robot is calibrated
    # or via start menu
    try:
        with open("balls.txt", "r") as f:
            number = int(f.readline())
        return number
    except BaseException:
        print("could not read balls.txt")
        return 3


def write_to_file(number: int):
    # counter part
    try:
        with open("balls.txt", "w") as f:
            f.write(str(number))
    except BaseException:
        print("could not save number to balls.txt")


def scan_for_ball() -> int:
    # do a 360 with the tof sensor
    # return the angle at which the ball is
    # ball is detected by the difference of the readings of the two sensors
    # check if it is a box rather than a ball
    # by reading sensor values at close angles
    # maybe go to a fixed distance to the detected object
    pass


def pick_up_ball(loc: int):
    # do a combination of drive closer and reading sensors and turning
    # than grab the ball, retry some times
    # should get some sort of sensor to test if the ball is in the grappler
    # look out for walls
    pass


def check_metal() -> bool:
    # as ez as a pin.value()
    pass


def search_for_box(type_of_ball: bool):
    # drive around the wall until you find a box
    # check if the color of the box matches with the type of ball
    # drop the ball yeeeeeeeees
    pass


def drive_around():
    # some type of move around in the room random and along the wall
    pass


def escape_room():
    number_balls_left = read_from_file()
    for _ in range(number_balls_left):
        while True:
            loc = scan_for_ball()
            if loc:
                pick_up_ball(loc)
                type_of_ball = check_metal()
                search_for_box(type_of_ball)
                break
            drive_around()

# notes
# check reflective an white sensors for silver, maybe better detection
