# void setup() {

#   Serial.begin(115200);

#   pinMode(SHCP, OUTPUT);
#   pinMode(STCP, OUTPUT);
#   pinMode(DS, OUTPUT);

#   pinMode(S0, OUTPUT);
#   pinMode(S1, OUTPUT);
#   pinMode(S2, OUTPUT);
#   pinMode(S3, OUTPUT);

#   pinMode(ADC_MULTI, INPUT);

#   ShiftRegisterReset();
# }

import pinesp32
from machine import Pin

S0 = Pin(pinesp32.S0, Pin.OUT)
S1 = Pin(pinesp32.S1, Pin.OUT)
S2 = Pin(pinesp32.S2, Pin.OUT)
S3 = Pin(pinesp32.S3, Pin.OUT)
SHCP = Pin(pinesp32.SHCP, Pin.OUT)
STCP = Pin(pinesp32.STCP, Pin.OUT)
DS = Pin(pinesp32.DS, Pin.OUT)
ADC_MULTI = Pin(pinesp32.ADC_MULTI, Pin.IN)

ShiftRegisterBits = [False]*24
