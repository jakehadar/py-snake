# -*- coding: utf-8 -*-

from snake.common import Point, Frame


class TestPoint:
    def test_eq(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        assert p1 == p2

    def test_not_eq(self):
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        assert p1 != p2

    def test_add1(self):
        p1 = Point(1, 1)
        p2 = Point(9, 9)
        assert p1 + p2 == Point(10, 10)

    def test_add2(self):
        p1 = Point(1, 2)
        p2 = Point(-1, -2)
        assert p1 + p2 == Point(0, 0)


class TestFrame:
    def test_height(self):
        frame = Frame(6, 12)
        assert frame.height == 12

    def test_width(self):
        frame = Frame(6, 12)
        assert frame.width == 6

    def test_surface_points(self):
        frame = Frame(2, 3)
        expected = {
            Point(x=0, y=0), Point(x=0, y=1),
            Point(x=1, y=1), Point(x=1, y=0),
            Point(x=0, y=2), Point(x=1, y=2)}
        assert frame.surface_points == expected

    def test_origin_point(self):
        frame = Frame(6, 12)
        assert frame.origin_point == Point(0, 0)

    def test_center_point(self):
        frame = Frame(6, 12)
        assert frame.center_point == Point(3, 6)

    def test_xrange(self):
        frame = Frame(2, 3)
        assert list(frame.xrange) == [0, 1]

    def test_yrange(self):
        frame = Frame(2, 3)
        assert list(frame.yrange) == [0, 1, 2]

    def test_contains(self):
        frame = Frame(2, 3)
        point = Point(1, 1)
        assert point in frame

    def test_not_contains1(self):
        frame = Frame(2, 3)
        point = Point(-1, -1)
        assert point not in frame

    def test_not_contains2(self):
        frame = Frame(2, 3)
        point = Point(2, 3)
        assert point not in frame
