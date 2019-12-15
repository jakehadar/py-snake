import os
from common import Point, format_seconds

NW, TOP, NE = '┌─┐'
LT, CTR, RT = '│ │'
SW, BTM, SE = '└─┘'
BODY = '█'
FOOD = '*'


class Canvas:
    def __init__(self, frame, model):
        self.frame = frame
        self.model = model
        self.grid = {}
        self.clear()

    def render(self, message=None):
        self.overlay(self.model.snake_body, BODY)
        self.overlay(self.model.food_locations, FOOD)
        self.overlay(self.model.available_locations, CTR)
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
        print(''.join([NW] + [TOP] * self.frame.width + [NE]))
        for y in self.frame.yrange:
            chars = [self.grid[Point(x, self.frame.height - y - 1)] for x in self.frame.xrange]
            print(''.join([LT] + chars + [RT]))
        print(''.join([SW] + [BTM] * self.frame.width + [SE]))
        print(f'Score: {self.model.score}')
