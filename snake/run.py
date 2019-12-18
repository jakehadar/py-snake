import os
import sys
import argparse

from .game import Game
from .config import GameConfig
from .common import GameOver
from .input import ArrowKeyReader as KeyReader

exit_func = sys.exit

PY_3 = sys.version_info.major == 3


def get_terminal_size_or_default(default, max_width=78, max_height=40):
    try:
        w, h = tuple(os.get_terminal_size())
        return min(w - 2, max_width), min(h - 5, max_height)

    except Exception:
        return default.width, default.height


def main():
    defaults = GameConfig()

    if PY_3:
        defaults.width, defaults.height = get_terminal_size_or_default(defaults)

    parser = argparse.ArgumentParser(description="Snake game for CLI")
    parser.add_argument("--width", type=int, help="Frame width", default=defaults.width)
    parser.add_argument("--height", type=int, help="Frame height", default=defaults.height)
    parser.add_argument("--speed", type=int, help="Snake speed (fps)", default=defaults.initial_speed)
    parser.add_argument("--food", type=int, help="Number of food pieces available", default=defaults.initial_food_count)
    args = parser.parse_args()

    max_food_count = defaults.max_food_count
    if args.food > defaults.max_food_count:
        max_food_count = args.food

    config = GameConfig()
    config.width = args.width
    config.height = args.height
    config.speed = args.speed
    config.initial_food_count = args.food
    config.max_food_count = max_food_count

    game = Game(config=config, key_reader_cls=KeyReader)

    try:
        game.run()
    except GameOver:
        return 0
    except Exception:
        raise
    # except Exception as e:
    #     print(e)
    # return 1


if __name__ == '__main__':
    exit_func(main())
