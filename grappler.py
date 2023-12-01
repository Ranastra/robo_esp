import servo

_servo_turn = servo.TWO
_servo_grab = servo.THREE


def up():
    servo.set_angle(_servo_turn, 90)


def down():
    servo.set_angle(_servo_turn, -90)


def grab():
    servo.set_angle(_servo_grab, 90)


def loose():
    servo.set_angle(_servo_grab, -90)
