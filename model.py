import warnings
import time

from common import Point, SelfCollision, BoundaryCollision, \
    IllegalDirectionTransition, DirectionOffset

__all__ = ['SnakeModel']


class DirectionState:
    UP = DirectionOffset.UP
    DOWN = DirectionOffset.DOWN
    LEFT = DirectionOffset.LEFT
    RIGHT = DirectionOffset.RIGHT

    legal_transitions = {
        UP: (LEFT, RIGHT),
        DOWN: (LEFT, RIGHT),
        LEFT: (UP, DOWN),
        RIGHT: (UP, DOWN)
    }

    def __init__(self, model, initial_direction=UP):
        self.model = model
        self._offset = initial_direction

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, proposed):
        if proposed not in self.legal_transitions[self.offset]:
            if len(self.model) > 1:
                warnings.warn("Snake cannot move this direction.", IllegalDirectionTransition)
                return

        self._offset = proposed


class SnakeModel:
    def __init__(self, frame, solid_walls=True):
        self.frame = frame
        self.snake_body = [frame.center_point + Point(0, -1 * int(frame.height / 4))]
        self.solid_walls = solid_walls
        self.direction = DirectionState(self)
        self.food_locations = []
        self.status_message = ''

    def step(self, should_grow=False):
        new_location = self.head_location + self.direction.offset

        if new_location in self:
            raise SelfCollision

        if self.solid_walls and new_location not in self.frame:
            raise BoundaryCollision

        self.snake_body.insert(0, new_location)

        if new_location in self.food_locations:
            self.food_locations.remove(new_location)
            should_grow = True

        if not should_grow:
            self.snake_body.pop()

        if not self.food_locations:
            location = self.available_locations.pop()
            self.food_locations.append(location)

    @property
    def head_location(self):
        return self.snake_body[0]

    @property
    def occupied_locations(self):
        return set(self.snake_body) | set(self.food_locations)

    @property
    def available_locations(self):
        return self.frame.surface_points - self.occupied_locations

    @property
    def score(self):
        return len(self.snake_body) - 1

    def __contains__(self, point):
        return point in self.snake_body

    def __len__(self):
        return len(self.snake_body)


def testme():
    from model import SnakeModel, DirectionOffset
    from common import Point
    s = SnakeModel(Point(5, 5), DirectionOffset.UP)
    s.step()
    s.grow()


if __name__ == '__main__':
    testme()
