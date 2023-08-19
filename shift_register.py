import machine
import pinesp32

_SHCP: machine.Pin = machine.Pin(pinesp32.SHCP, machine.Pin.OUT)
_STCP: machine.Pin = machine.Pin(pinesp32.STCP, machine.Pin.OUT)
_DS: machine.Pin = machine.Pin(pinesp32.DS, machine.Pin.OUT)

_shift_register_bits: list[bool] = [False]*24

# note: 3 shift registers * 8, 24 addr
# DS data serial, SHCP clock serial pin, STCP storage serial pin


def write():
    _STCP.value(0)
    for i in range(23, -1, -1):
        _SHCP.value(0)
        _DS.value(_shift_register_bits[i])
        _SHCP.value(1)
    _STCP.value(1)


def set(pin: int, state: bool):
    _shift_register_bits[pin] = state


def reset():
    _STCP.value(0)
    for _ in range(24):
        _SHCP.value(0)
        _DS.value(0)
        _SHCP.value(1)
    _STCP.value(1)
