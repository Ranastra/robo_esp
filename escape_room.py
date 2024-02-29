import time
import lightsensor
import led
import grappler
import color
import gyro
import pinesp32
import tof
import motor
import tof
import linefollower
import button


def run():
    drive_in_escape_room(0)
    escape_room_without_balls()


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


def drive_forward_until(f, v: int):
    led.set_status_left(led.RED)
    motor.stop(motor.MOT_AB)
    gyro.reset()
    motor.drive(motor.MOT_AB, v)
    while f():
        gyro.update()
        # motor.drive(motor.MOT_A, v + 10*abs(gyro.angle[2]))
        # motor.drive(motor.MOT_A, v - 10*abs(gyro.angle[2]))


def drive_in_escape_room(recursion):
    """drive until both sensors see silver"""
    led.set_status_left(led.BLUE)
    vals = lightsensor.silver()
    print("tse")
    motor.drive(motor.MOT_AB, -60)
    time.sleep_ms(300)
    motor.stop(motor.MOT_AB)
    if vals[0]:
        motor.drive(motor.MOT_B, 90)
        while not vals[1]:
            lightsensor.measure_reflective()
            vals = lightsensor.silver()
    if vals[1]:
        motor.drive(motor.MOT_A, 90)
        while not vals[0]:
            lightsensor.measure_reflective()
            vals = lightsensor.silver()
    motor.stop(motor.MOT_AB)
    if recursion:
        motor.drive(motor.MOT_AB, -60)
        time.sleep_ms(600)
        for _ in range(5):
            lightsensor.measure_reflective()

        def until_silver() -> bool:
            lightsensor.measure_reflective()
            return not lightsensor.on_silver()
        drive_forward_until(until_silver, 60)
        # time.sleep_ms(300)
        motor.stop(motor.MOT_AB)
        drive_in_escape_room(recursion-1)


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


def wall_follower():
    tof.set(tof.FOUR)
    while True:
        diff = 50 - tof.read()
        # thats the formula to make gold with hay
        motor.drive(motor.MOT_A, 50 - 11*diff/(abs(diff)**0.7+1))
        motor.drive(motor.MOT_B, 50 + 11*diff/(abs(diff)**0.7+1))


def escape_room_without_balls():
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.RED)
    time.sleep_ms(3000)
    # follow the wall
    motor.drive(motor.MOT_AB, 70)
    time.sleep_ms(1000)
    linefollower.drive_angle(90)
    motor.drive(motor.MOT_AB, 70)
    time.sleep_ms(1000)
    motor.stop(motor.MOT_AB)
    tof.set(tof.FOUR)
    while True:
        while True:
            dist = 70 - tof.read()
            lightsensor.measure_white()
            # motor.drive(motor.MOT_A, 80 - int(2*dist/(abs(dist)**0.5))//1)
            # motor.drive(motor.MOT_B, 80 + int(2*dist/(abs(dist)**0.5))//1)
            motor.drive(motor.MOT_A, 65 - 7*dist/(abs(dist)**0.6+1))
            motor.drive(motor.MOT_B, 65 + 7*dist/(abs(dist)**0.6+1))
            if not lightsensor.all_white():
                motor.stop(motor.MOT_AB)
                time.sleep_ms(2000)
                return
            if not button.left() or not button.right():
                if button.left():
                    while not button.right():
                        motor.drive(motor.MOT_B, 70)
                        motor.drive(motor.MOT_A, 30)
                else:
                    while not button.left():
                        motor.drive(motor.MOT_A, 70)
                        motor.drive(motor.MOT_B, 70)
                break
            # if abs(dist) >= 1000:
            #     motor.stop(motor.MOT_AB)
            #     led.set_status_locked(2, led.RED)
            #     time.sleep_ms(3000)
            #     led.set_status_locked(2, led.GREEN)
        motor.drive(motor.MOT_AB, -70)
        time.sleep_ms(300)
        linefollower.drive_angle(-90)


        # notes
        # check reflective an white sensors for silver, maybe better detection
        # motor trimmen TODO
if __name__ == "__main__":
    # baaaaallll()
    test_drive_360()
