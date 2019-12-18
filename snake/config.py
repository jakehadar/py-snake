import os
import sys

default_frame = (25, 10)

if sys.version_info.major == 3:
    try:
        w, h = tuple(os.get_terminal_size())
        default_frame = (w - 2, h - 5)
    except:
        pass


class GameConfig:
    width, height = default_frame
    initial_speed = 3.0
    max_speed = 30
    speed_increase_factor = 0.15
    solid_walls = True

    # Amount of food initially displayed on screen.
    initial_food_count = 1
    max_food_count = 5

    # Increment food_count for every N points scored.
    # (Set this to 0 to keep food_count unchanged).
    food_increase_interval = 10