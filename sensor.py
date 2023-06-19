import pinesp32 as p

class Sensor():
    def __init__(self, channel_number:int):
        self.channel = channel_number
        self.min_val = 0
        self.max_val = 65536
        self.val = 0

    def map_raw_value(self) -> int:
        return ((self.val - self.min_val) * 100) // (self.max_val - self.min_val)


all_sensors = [Sensor(p.ADC_PT_REF_L), Sensor(p.ADC_PT_L_1), Sensor(p.ADC_PT_L_0),
               Sensor(p.ADC_PT_M), Sensor(p.ADC_PT_R_0), Sensor(p.ADC_PT_R_1), Sensor(p.ADC_PT_REF_R)]

green_sensors = [Sensor(p.ADC_PT_L_1), Sensor(p.ADC_PT_L_0), Sensor(p.ADC_PT_R_0), Sensor(p.ADC_PT_R_1)]

red_sensors = [Sensor(p.ADC_PT_L_1), Sensor(p.ADC_PT_L_0), Sensor(p.ADC_PT_R_0), Sensor(p.ADC_PT_R_1)]
