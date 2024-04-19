import servo

_servo_turn = servo.THREE
_servo_grab = servo.FOUR


def up():
    for i in range(-90, 91, 15):
        servo.set_angle(_servo_turn, -i, wait_time_ms=100)
    # servo.set_angle(_servo_turn, -90)


def down():
    servo.set_angle(_servo_turn, 90)


def grab():
    for i in range(-90, 91, 15):
        servo.set_angle(_servo_grab, -i, wait_time_ms=100)
    # servo.set_angle(_servo_grab, -90)


def loose():
    servo.set_angle(_servo_grab, 30)  
