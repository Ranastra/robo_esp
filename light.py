import pinesp32
from time import sleep_ms
from machine import Pin, ADC
from shift_register import shift_register_write, shift_register_set, shift_register_reset
shift_register_reset()

# c++ https://github.com/waspinator/CD74HC4067

_g_channel_truth_table = [
    # s0, s1, s2, s3     channel
    [0,  0,  0,  0],  # 0
    [1,  0,  0,  0],  # 1
    [0,  1,  0,  0],  # 2
    [1,  1,  0,  0],  # 3
    [0,  0,  1,  0],  # 4
    [1,  0,  1,  0],  # 5
    [0,  1,  1,  0],  # 6
    [1,  1,  1,  0],  # 7
    [0,  0,  0,  1],  # 8
    [1,  0,  0,  1],  # 9
    [0,  1,  0,  1],  # 10
    [1,  1,  0,  1],  # 11
    [0,  0,  1,  1],  # 12
    [1,  0,  1,  1],  # 13
    [0,  1,  1,  1],  # 14
    [1,  1,  1,  1]   # 15
]

_S0 = Pin(pinesp32.S0, Pin.OUT)
_S1 = Pin(pinesp32.S1, Pin.OUT)
_S2 = Pin(pinesp32.S2, Pin.OUT)
_S3 = Pin(pinesp32.S3, Pin.OUT)
_ADC_MULTI = ADC(Pin(pinesp32.ADC_MULTI, Pin.IN))

def set_channel(channel: int):
    _S0.value(_g_channel_truth_table[channel][0])
    _S1.value(_g_channel_truth_table[channel][1])
    _S2.value(_g_channel_truth_table[channel][2])
    _S3.value(_g_channel_truth_table[channel][3])

def read_raw(channel: int):
    set_channel(channel)
    return _ADC_MULTI.read_u16()

print("te")
print(read_raw(pinesp32.ADC_PT_M))
print("te")
while True:
    sleep_ms(200)
    print(read_raw(pinesp32.ADC_PT_M))