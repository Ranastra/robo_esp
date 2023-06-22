from machine import Pin, I2C
import time
from pinesp32 import SCL, SDA

i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA))

while True:
    print("Scanning...")
    devices = i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found")
    else:
        for address in devices:
            print("I2C device found at address 0x{:02X}!".format(address))
    print("Done\n")
    time.sleep(5)  # Wait 5 seconds for the next scan
