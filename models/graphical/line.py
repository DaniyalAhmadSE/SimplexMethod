from typing import List
from models.point2d import Point2D as Point


class Line:
    def __init__(self, Point2D_a: Point, Point2D_b: Point) -> None:
        self._Point2D_a = Point2D_a
        self._Point2D_b = Point2D_b

    def get_Point2D_a(self) -> Point:
        return self._Point2D_a

    def set_Point2D_a(self, Point2D_a: Point) -> None:
        self._Point2D_a = Point2D_a

    def get_Point2D_b(self) -> Point:
        return self._Point2D_b

    def set_Point2D_b(self, Point2D_b: Point) -> None:
        self._Point2D_b = Point2D_b

    def get_points(self) -> List[Point]:
        return [self._Point2D_a, self._Point2D_b]

    Point2D_a: Point = property(get_Point2D_a, set_Point2D_a)
    Point2D_b: Point = property(get_Point2D_b, set_Point2D_b)
    points: List[Point] = property(get_points)
