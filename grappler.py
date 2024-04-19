import servo

_servo_turn = servo.TWO
_servo_grab = servo.ONE


def up():
    for i in range(-90, 91, 15):
        servo.set_angle(_servo_turn, -i, wait_time_ms=100)
    # servo.set_angle(_servo_turn, -90)


def down():
    servo.set_angle(_servo_turn, 10)


def grab():
    for i in range(-90, 91, 15):
        servo.set_angle(_servo_grab, -i, wait_time_ms=100)
    # servo.set_angle(_servo_grab, -90)


def loose():
    servo.set_angle(_servo_grab, 30)  

def throw():
    servo.set_angle(_servo_turn, 0, wait_time_ms=1)
    servo.set_angle(_servo_grab, 30, wait_time_ms=1)
    


if __name__ == '__main__':
    up()
    down()
    up()
    down()
