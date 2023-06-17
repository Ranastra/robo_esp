import pinesp32
from machine import Pin, ADC
from shift_register import shift_register_write, shift_register_set

# c++ https://github.com/waspinator/CD74HC4067

_g_channel_truth_table = [
    #s0, s1, s2, s3     channel
    [1,  1,  1,  1],  # 0
    [0,  1,  1,  1],  # 1
    [1,  0,  1,  1],  # 2
    [0,  0,  1,  1],  # 3
    [1,  1,  0,  1],  # 4
    [0,  1,  0,  1],  # 5
    [1,  0,  0,  1],  # 6
    [0,  0,  0,  1],  # 7
    [1,  1,  1,  0],  # 8
    [0,  1,  1,  0],  # 9
    [1,  0,  1,  0],  # 10
    [0,  0,  1,  0],  # 11
    [1,  1,  0,  0],  # 12
    [0,  1,  0,  0],  # 13
    [1,  0,  0,  0],  # 14
    [0,  0,  0,  0]   # 15
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

while True:
    print(read_raw(pinesp32.ADC_PT_M))