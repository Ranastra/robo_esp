import pinesp32


class Sensor():
    def __init__(self, channel_number: int):
        self.channel = channel_number
        self.min_val = 0
        self.max_val = 65536
        self.val = 0

    def map_raw_value(self) -> int:
        return ((self.val - self.min_val) * 100) // (self.max_val - self.min_val)


all = [
    Sensor(pinesp32.ADC_PT_REF_L),
    Sensor(pinesp32.ADC_PT_L_1),
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_M),
    Sensor(pinesp32.ADC_PT_R_0),
    Sensor(pinesp32.ADC_PT_R_1),
    Sensor(pinesp32.ADC_PT_REF_R)
]

green = [
    Sensor(pinesp32.ADC_PT_L_1),
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_R_0),
    Sensor(pinesp32.ADC_PT_R_1)
]

red = [
    Sensor(pinesp32.ADC_PT_L_1),
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_R_0),
    Sensor(pinesp32.ADC_PT_R_1)
]
