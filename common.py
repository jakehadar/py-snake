from functools import lru_cache
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __eq__(self, other): return self.x == other.x and self.y == other.y
    def __add__(self, other): return Point(self.x + other.x, self.y + other.y)
    def __hash__(self): return hash(str(self))


class Frame(NamedTuple):
    width: int
    height: int
    x: int = 0
    y: int = 0

    @property
    def origin_point(self):
        return Point(self.x, self.y)

    @property
    def center_point(self):
        return Point(int(self.width / 2), int(self.height / 2))

    @property
    @lru_cache()
    def surface_points(self):
        return set(Point(x, y) for x in self.xrange for y in self.yrange)

    @property
    def xrange(self):
        return range(self.origin_point.x, self.origin_point.x + self.width)

    @property
    def yrange(self):
        return range(self.origin_point.y, self.origin_point.y + self.height)

    def __contains__(self, point):
        return point in self.surface_points


class DirectionOffset:
    UP = Point(0, 1)
    DOWN = Point(0, -1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)


class GameConfig(NamedTuple):
    width: int = 25
    height: int = 10
    initial_speed: int = 3
    speed_increase_factor = 0.15
    solid_walls: bool = True

    # Amount of food initially displayed on screen.
    food_count: int = 1

    # Increment food_count for every N points scored.
    # (Set this to 0 to keep food_count unchanged).
    food_increase_interval: int = 5


def format_seconds(seconds, fmt_str='{m}:{s:02d}'):
    m = int(seconds / 60)
    s = int(seconds - m * 60)
    return fmt_str.format(m=m, s=s)


class SelfCollision(Exception):
    pass


class BoundaryCollision(Exception):
    pass


class IllegalDirectionTransition(Warning):
    pass

