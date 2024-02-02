import time
import lightsensor
import led
import grappler
import color
import gyro
import pinesp32
import tof
import motor


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


def test_drive_360():
    motor.drive(motor.MOT_A, 50)
    motor.drive(motor.MOT_B, -50)
    tof.set(tof.TWO)
    last = tof.read()
    avg = last
    while True:
        while last == tof.read():
            pass
        now = tof.read()
        print(now, last / avg, avg)
        avg = (last * 2 + now) / 3
        last = now


def baaaaallll():
    motor.drive(motor.MOT_A, 80)
    motor.drive(motor.MOT_B, -80)
    tof.set(tof.TWO)
    upper = tof.read()
    tof.set(tof.THREE)
    lower = tof.read()
    diff_av = upper - lower
    while True:
        tof.set(tof.TWO)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        diff = upper-lower
        if upper < 700:
            # if True:
            diff_av = diff_av * 0.5 + diff * 0.5
            if diff_av * 2 < diff:
                print("BALLLLLLLl")
                # break
        print(upper, lower, diff, upper / lower)
    print("stop")
    motor.stop(motor.MOT_AB)
    time.sleep_ms(500)
    # dir_flag = 1
    # while tof.read() > 50:
    #     motor.drive(motor.MOT_AB, 70)
    #     print("vorne")
    #     time.sleep_ms(300)
    #     motor.stop(motor.MOT_AB)
    #     goal = tof.read() + 10
    #     while True:
    #         lower = tof.read()
    #         if lower > goal:
    #             break
    #         motor.drive(motor.MOT_A, dir_flag*100)
    #         motor.drive(motor.MOT_B, -dir_flag*100)
    #         time.sleep_ms(100)
    #         motor.stop(motor.MOT_AB)
    #         time.sleep_ms(200)
    #     dir_flag *= -1
    # print("stop")
    motor.stop(motor.MOT_AB)
    # motor.drive(motor.MOT_A, 70)
    # motor.drive(motor.MOT_B, -70)


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
if __name__ == "__main__":
    # baaaaallll()
    test_drive_360()
