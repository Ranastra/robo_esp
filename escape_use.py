import motor
import led
import utime
import gyro
import tof
import lightsensor
import button

# tof.TWO = upper
# tof.THREE = lower

def sign(x: float):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def is_outside():
    lightsensor.measure_white()
    lightsensor.measure_reflective()
    # return False
    return lightsensor.silver()[0] or lightsensor.silver()[1] or not lightsensor.all_white()
    

def get_angle(angle: float, base_v: int):
    def inner() -> bool:
        gyro.update()
        return abs(gyro.angle[2]) > angle
    motor.stop(motor.MOT_AB)
    gyro.reset()
    angle = angle - gyro.angle[2] # relative angle is better
    s = sign(angle)
    angle *= s
    motor.drive(motor.MOT_A, s * base_v)
    motor.drive(motor.MOT_B, -s * base_v)
    return inner


def get_timeout(t: int):
    def inner() -> bool:
        return utime.ticks_ms() > end
    end = utime.ticks_ms() + t
    return inner

def just_drive_angle(angle: float, t: int):
    # print("in just_drive_angle", angle)
    a = get_angle(angle, 70)
    timeout = get_timeout(t)
    while not a() and not timeout():
        pass
    motor.stop(motor.MOT_AB)

def just_drive_forward(t: int, rev = 1):
    motor.drive(motor.MOT_AB, rev * 70)
    timeout = get_timeout(t)
    while not timeout():
        pass
    motor.stop(motor.MOT_AB)

def try_scan() -> list[tuple[float, float, float]]:
    led.set_status_locked(2, led.RED)
    angle = get_angle(angle=180.0, base_v=40)
    time_out = get_timeout(t=7000)
    data = []
    while not angle() and not time_out():
        tof.set(tof.TWO)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        data.append((upper, lower, gyro.angle[2]))
    just_drive_angle(-gyro.angle[2], 4500)
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.GREEN)
    return data

def check_diff(data: list[tuple[float, float, float]]) -> float:
    LIMIT_DIFF = 100.0
    OUT_OF_MAP_LIMIT = 1500.0
    max_diff = LIMIT_DIFF
    angle = 0.0
    for i in range(len(data)):
        if data[i][0] - data[i][1] > max_diff and data[i][0] < OUT_OF_MAP_LIMIT:
            max_diff = data[i][0] - data[i][1]
            angle = data[i][2]
    return angle

def get_lowest(data: list[tuple[float, float, float]]) -> float:
    lowest = 4000.0
    lowest_angle = -1.0
    for i in range(len(data)):
        if data[i][0] < lowest:
            lowest = data[i][0]
            lowest_angle = data[i][2]
    # print("in get_lowest")
    # print("data: ", data)
    # print("lowest_angle", lowest_angle)
    return lowest_angle

def drive_at_wall():
    led.set_status_locked(2, led.PURPLE)
    motor.drive(motor.MOT_AB, 50)
    timeout = get_timeout(900)
    while not timeout():
        if is_outside():
            just_drive_forward(700, rev=-1)
            just_drive_angle(90.0, 1000)
        if not button.right.value() or not button.left.value():
            just_drive_forward(300, rev=-1)
            just_drive_angle(90.0, 1000)
    motor.stop(motor.MOT_AB)


def run():
    while True:
        drive_at_wall()
        data = try_scan()
        ball_angle = check_diff(data)
        # print(" in run ball angle", ball_angle)
        if ball_angle:
            just_drive_angle(ball_angle, 1000)
            motor.stop(motor.MOT_AB)
            led.set_status_locked(2, led.YELLOW)
            utime.sleep_ms(1500)
            # grappler runter und aufmachen :)
            motor.drive(motor.MOT_AB, 50)
            timeout = get_timeout(2000)
            while not timeout():
                if is_outside(): 
                    break
            motor.stop(motor.MOT_AB)
            # grappler zu und hoch!!!
            utime.sleep_ms(1000)
        else:
            # wall_angle = get_lowest(data)
            # # print(" in run wall angle", wall_angle)
            # just_drive_angle(wall_angle, 1000)
            pass
            
