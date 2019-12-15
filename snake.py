import sys
import argparse

from snake.game import Game, GameConfig


def main():
    defaults = GameConfig()
    parser = argparse.ArgumentParser(description="Snake game for CLI")
    parser.add_argument("--width", type=int, help="Frame width", default=defaults.width)
    parser.add_argument("--height", type=int, help="Frame height", default=defaults.height)
    parser.add_argument("--speed", type=int, help="Snake speed (fps)", default=defaults.initial_speed)
    parser.add_argument("--food", type=int, help="Number of food pieces available", default=defaults.initial_food_count)
    args = parser.parse_args()

    max_food_count = defaults.max_food_count
    if args.food > defaults.max_food_count:
        max_food_count = args.food

    config = GameConfig(args.width, args.height, args.speed,
                        initial_food_count=args.food, max_food_count=max_food_count)
    game = Game(config=config)
    game.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
