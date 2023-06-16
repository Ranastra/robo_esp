# main.py -- put your code here!
#from led import loop
#loop()
from machine import Pin, ADC

class Mux:
    def __init__(self, S0, S1, S2, S3, E, signal=0):
        self.S0 = Pin(S0, Pin.OUT)
        self.S1 = Pin(S1, Pin.OUT)
        self.S2 = Pin(S2, Pin.OUT)
        self.S3 = Pin(S3, Pin.OUT)
        self.E = Pin(E, Pin.IN)
        self.signal = ADC(self.E)
        self._reset()
        self.current_bits = "0000"
        self.state = False
    
    def _reset(self):
        self.S0.off()
        self.S1.off()  
        self.S2.off()  
        self.S3.off()  
        self.E.off()

    def switch_state(self):
        if self.state:
            self.E(0)
            self.state = False
        else:
            self.E(1)
            self.state = True

    def _bits_to_channel(self, bits):
        return int("0000" + "".join([str(x) for x in "".join(reversed(bits))]), 2)

    def _channel_to_bits(self, channel_id):
        return ''.join(reversed("{:0>{w}}".format(bin(channel_id)[2:], w=4)))
    
    def _switch_pins_with_bits(self, bits):  
        s0, s1, s2, s3 = [int(x) for x in tuple(bits)]  
        self.S0(s0)  
        self.S1(s1)  
        self.S2(s2)  
        self.S3(s3)

    def switch_channel(self, channel_id):  
        bits = self._channel_to_bits(channel_id)  
        self._switch_pins_with_bits(bits)  
        self.current_bits = bits


from pinesp32 import S0, S1, S2, S3, ADC_MULTI
mux = Mux(S0, S1, S2, S3, ADC_MULTI)
from pinesp32 import ADC_PT_M
mux.switch_state()
mux.switch_channel(ADC_PT_M)
print("test")
# while True: print(mux.signal.read())