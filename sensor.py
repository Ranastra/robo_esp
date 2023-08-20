import pinesp32


class Sensor():
    """Sensor class, for one phototransistor"""

    def __init__(self, channel_number: int):
        self.channel = channel_number
        self.min = 0
        self.max = 4096
        self.val = 0

    def map_raw_value(self) -> int:
        """ map raw value to range 0-100"""
        return ((self.val - self.min) * 100) // (self.max - self.min)


# Sensor instances

white = [
    Sensor(pinesp32.ADC_PT_L_1),
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_M),
    Sensor(pinesp32.ADC_PT_R_0),
    Sensor(pinesp32.ADC_PT_R_1),
]

green = [
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_R_0),
]

red = [
    Sensor(pinesp32.ADC_PT_L_0),
    Sensor(pinesp32.ADC_PT_R_0),
]

silver = [
    Sensor(pinesp32.ADC_PT_REF_L),
    Sensor(pinesp32.ADC_PT_REF_R),
]
