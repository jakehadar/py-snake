import os
from snake.common import Point

NW, TOP, NE = '┌─┐'
LT, CTR, RT = '│ │'
SW, BTM, SE = '└─┘'
BODY = '█'
FOOD = '*'


class Canvas:
    def __init__(self, frame, model, game):
        self.frame = frame
        self.model = model
        self.game = game
        self.grid = {}
        self.clear()

    def render(self, message=None):
        self.overlay(self.model.snake_body, BODY)
        self.overlay(self.model.food_locations, FOOD)
        self.overlay(self.model.empty_locations, CTR)
        if message:
            for i, char in enumerate(message):
                x_offset = -1 * int(len(message) / 2) + i
                y_offset = -1 * int(self.frame.height / 4)
                self.overlay([self.frame.center_point + Point(x_offset, 0)], char)
        self.print()

    def clear(self):
        self.grid = {point: CTR for point in self.frame.surface_points}

    def overlay(self, points, char):
        for point in points:
            self.grid[point] = char

    def print(self):
        os.system('clear')
        speed_text = f'Speed: {self.game.speed:.02f}'
        coverage_text = f'Cov: {(len(self.model) / len(self.frame.surface_points) * 100):.0f}%'
        print(f'{speed_text} {coverage_text.rjust(self.frame.width - len(speed_text) + 1, CTR)}')
        print(''.join([NW] + [TOP] * self.frame.width + [NE]))
        for y in self.frame.yrange:
            chars = [self.grid[Point(x, self.frame.height - y - 1)] for x in self.frame.xrange]
            print(''.join([LT] + chars + [RT]))
        print(''.join([SW] + [BTM] * self.frame.width + [SE]))
        print(f'Score: {self.model.score}')
