import pinesp32
import utime
import shift_register
import i2c
import vl53l1x


TOF = int
ONE: TOF = pinesp32.SR_XSHT1
TWO: TOF = pinesp32.SR_XSHT2
THREE: TOF = pinesp32.SR_XSHT3
FOUR: TOF = pinesp32.SR_XSHT4

shift_register.set(TWO, True)
shift_register.set(FOUR, False)
shift_register.set(THREE, False)
shift_register.set(ONE, False)
shift_register.write()
_current = TWO
utime.sleep_ms(50)

_TOF = vl53l1x.VL53L1X(i2c.I2C)
utime.sleep_ms(50)


def set(tof: TOF):
    global _current
    if _current != tof:
        shift_register.set(_current, False)
        _current = tof
        shift_register.set(tof, True)
        shift_register.write()
        utime.sleep_ms(2)
        _TOF.try_reset()
        start = utime.ticks_ms()
        while start + 2000 > utime.ticks_ms() and read() == 0:
            pass


def read() -> int:
    return _TOF.read()


def test(tof: TOF):
    set(tof)
    while True:
        print(read())
        utime.sleep_ms(200)


def test_one(tof: TOF):
    set(tof)
    while True:
        print(read())
        utime.sleep_ms(200)


def test_two_three():
    while True:
        set(THREE)
        print("three", read(), end="###")
        set(TWO)
        print("two", read())


def time_it():
    start = utime.ticks_ms()
    set(THREE)
    for _ in range(10):
        set(TWO)
        read()
        set(THREE)
        read()
    print((utime.ticks_ms() - start)/20)


def time_one():
    set(TWO)
    l = [0]
    start = utime.ticks_ms()
    for _ in range(20):
        while read() == l[-1]:
            pass
        l.append(read())
    print((utime.ticks_ms() - start) / 20)
    print(l)


if __name__ == "__main__":
    # test_one(TWO)
    # test_two_three()
    # test()
    # time_it()
    time_one()
