import motor
import tof
import gyro
import lightsensor
import grappler
import random
import time
import led


def sign(num: int):
    """no inbuild sign function"""
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def drive_angle(angle: int, base_v=100, reset=True, overwrite=False) -> bool:
    motor.stop(motor.MOT_AB)
    if reset:
        gyro.reset()
    s = sign(angle)
    angle *= s
    if not overwrite:
        motor.drive(motor.MOT_A, s * (base_v + 10))
        motor.drive(motor.MOT_B, - s * (base_v - 10))
    else:
        motor.drive(motor.MOT_B, -s * 40)
        motor.drive(motor.MOT_A, s * 60)

    def inner() -> bool:
        gyro.update()
        return abs(gyro.angle[2]) > angle
    return inner


def timeout(t: int):
    end = time.ticks_ms() + t

    def inner() -> bool:
        return time.ticks_ms() > end

    return inner


def out_of_box():
    def inner() -> bool:
        lightsensor.measure_white()
        lightsensor.measure_reflective()
        return not lightsensor.all_white() or lightsensor.silver()
    return inner


def scan():
    # time_out = timeout(15_000)
    angle = drive_angle(360, overwrite=True)
    data = []
    # while not angle() and not time_out():
    while not angle():
        tof.set(tof.TWO)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        data.append((upper, lower, gyro.angle[2]))
    motor.stop(motor.MOT_AB)
    return data


def write_data(data: list[tuple[int, int, int]], file: str):
    try:
        with open(file, 'a') as f:
            f.write(str(data) + "\n")
    except BaseException:
        print("can not write to tof data file")


def decide_ball(data: list[tuple[int, int, int]]) -> int:
    # normalize input
    print_flag = True
    max_val_u, min_val_u = max([d[0] for d in data]), min([d[0] for d in data])
    max_val_l, min_val_l = max([d[1] for d in data]), min([d[1] for d in data])
    norm_upper = [(d[0] - min_val_u) * 100 // (max_val_u - min_val_u)
                  for d in data]
    norm_lower = [(d[1] - min_val_l) * 100 // (max_val_l - min_val_l)
                  for d in data]
    dist = [norm_upper[0] - norm_lower[0]]
    dist_delta = []
    for i in range(1, len(data)):
        dist.append(norm_upper[i] - norm_lower[i])
        dist_delta.append(dist[i-1] - dist[i])
    angle = [d[2] for d in data]
    if print_flag:
        # if False:
        print('angle ', angle)
        print('upper ', [d[0] for d in data])
        print('lower ', [d[1] for d in data])
        print('norm_upper ', norm_upper)
        print('norm_lower ', norm_lower)
        print('dist ', dist)
        print('dist_delta ', dist_delta)
    max_delta_dist = 0
    min_delta_dist = 0
    for i in range(len(dist_delta)):
        if dist_delta[max_delta_dist] < dist_delta[i]:
            max_delta_dist = i
    if print_flag:
        print('max ', angle[max_delta_dist], ' min ', angle[min_delta_dist])
    write_data(dist_delta, "delta_dist.txt")
    write_data(dist, "dist.txt")
    return angle[max_delta_dist], data[max_delta_dist][1]


def drive_until_tof(the_tof: tof.TOF, lower_limit: int):
    tof.set(the_tof)
    motor.drive(motor.MOT_AB, 100)

    def inner() -> bool:
        return tof.read() < lower_limit
    return inner


def run():
    motor.stop(motor.MOT_AB)
    while True:
        angle = drive_angle(random.randint(-30, 30))
        motor.drive(motor.MOT_AB, 100)
        time_out = timeout(random.randint(200, 600))
        while not angle() and not time_out():
            pass
        motor.stop(motor.MOT_AB)
        while True:
            led.set_status_locked(2, led.WHITE)
            val = scan()
            print(val)
            motor.stop(motor.MOT_AB)
            time.sleep_ms(1_000)
            write_data(val, "raw_tof.txt")
            angle, lower = decide_ball(val)
            if angle > 180:
                angle = 360 - 180
            else:
                angle += 10
            led.set_status_locked(2, led.GREEN)
            time.sleep_ms(1_000)
            angle = drive_angle(angle, reset=True)
            while not angle():
                pass
            motor.stop(motor.MOT_AB)
            led.set_status_locked(2, led.PURPLE)
            time.sleep_ms(2_000)
            # drive_tof = drive_until_tof(tof.TWO, 50)
            # while not drive_tof():
            #     pass
            motor.stop(motor.MOT_AB)
            grappler.down()
            grappler.grab()
            led.set_status_locked(2, led.RED)


def test_angle():
    angle = drive_angle(90)
    while not angle():
        pass
    motor.stop(motor.MOT_AB)
    print(gyro.angle)
