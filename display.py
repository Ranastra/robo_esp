import i2c
import ssd1306

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

_DISPLAY = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c.I2C)


def log(msg):
    """log message to display"""
    _DISPLAY.text(msg, 0, 0)
    _DISPLAY.show()
