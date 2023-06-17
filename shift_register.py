from machine import Pin
import pinesp32

SHCP:Pin = Pin(pinesp32.SHCP, Pin.OUT)
STCP:Pin = Pin(pinesp32.STCP, Pin.OUT)
DS:Pin = Pin(pinesp32.DS, Pin.OUT)

_shift_register_bits:list[bool] = [False]*24

def shift_register_write():
    STCP.value(0)
    for i in range(23, -1, -1):
        SHCP.value(0)
        DS.value(_shift_register_bits[i])
        SHCP.value(1)
    STCP.value(1)

def shift_register_set(pin:int, state:bool):
    _shift_register_bits[pin] = state

def shift_register_reset():
    STCP.value(0)
    for _ in range(24):
        SHCP.value(0)
        DS.value(0)
        SHCP.value(1)
    STCP.value(1)