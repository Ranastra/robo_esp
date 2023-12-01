import lightsensor
import led
import time

# hopes that serves separation of concerns
# somewhere here will live the color stuff for escape room too

_RED_GREEN_DIFF_GREEN_LEVEL: int = 10  # green when value lower
_RED_GREEN_DIFF_RED_LEVEL: int = -60  # red when value higher
_WHITE_LEVEL_GREEN: int = 50

# _GREEN_COUNT_LEVEL: int = 7
_GREEN_COUNT_LEVEL: int = 7
# _RED_COUNT_LEVEL: int = 10
_RED_COUNT_LEVEL: int = 10


class _Green_Counters():
    def __init__(self):
        self.count_no_green = 20
        self.count_green = 0
        self.count_red = 0
        self.green = False


_left_right = [_Green_Counters(), _Green_Counters()]


def get() -> list[lightsensor.COLOR]:
    """update counters for colors0 and return them as list"""
    diff = lightsensor.get_green_red_diff()
    green = lightsensor.get_green()
    colors = [lightsensor.WHITE, lightsensor.WHITE]
    for i in range(2):
        if diff[i] > _RED_GREEN_DIFF_GREEN_LEVEL:
            _left_right[i].count_green += 1
            if _left_right[i].count_green > _GREEN_COUNT_LEVEL:
                _left_right[i].count_green = 0
                _left_right[i].green = True
                if i == 1:
                    led.set_status_right_locked(led.GREEN)
                else:
                    led.set_status_left_locked(led.GREEN)
        elif diff[i] < _RED_GREEN_DIFF_RED_LEVEL:
            _left_right[i].count_red += 1
            if _left_right[i].count_red > _RED_COUNT_LEVEL:
                if i == 1:
                    led.set_status_right_locked(led.RED)
                else:
                    led.set_status_left_locked(led.RED)
                colors[i] = lightsensor.RED
                continue
        else:
            _left_right[i].count_no_green += 1
            if _left_right[i].count_no_green > _GREEN_COUNT_LEVEL:
                _left_right[i].green = False
                _left_right[i].count_green = 0
                _left_right[i].count_red = 0
        if not _left_right[i].green:
            if green[i] > _WHITE_LEVEL_GREEN:
                colors[i] = lightsensor.WHITE
            else:
                colors[i] = lightsensor.BLACK
        else:
            colors[i] = lightsensor.GREEN
    return colors


def reset():
    _left_right[0] = _Green_Counters()
    _left_right[1] = _Green_Counters()


def test():
    while True:
        for _ in range(10):
            lightsensor.measure_green_red()
        print("colors: ", [lightsensor.color_map[num] for num in get()])
        print("green: ", lightsensor.get_green())
        print("diffs: ", lightsensor.get_green_red_diff())
        time.sleep_ms(20)
