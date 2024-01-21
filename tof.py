import pinesp32
import shift_register
import shift_register
import i2c


TOF = int

active: TOF = 0

ONE: TOF = pinesp32.SR_XSHT1
TWO: TOF = pinesp32.SR_XSHT2
THREE: TOF = pinesp32.SR_AIN1
FOUR: TOF = pinesp32.SR_AIN2


# def measure(tof: TOF):
#     global active
#     if active != tof:
#         shift_register.set(active, False)
#         active = tof


def test():
    shift_register.set(TWO, True)
    shift_register.write()
    # i2c.test()
