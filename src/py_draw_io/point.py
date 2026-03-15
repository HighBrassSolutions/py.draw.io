from .boundary_container import BoundaryContainer
from .fittable import Fittable
from typing import Any


class Point(Fittable):
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            raise TypeError(f"Cannot compare Point with {type(other)}")
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Any) -> Point:
        if not isinstance(other, Point):
            raise TypeError(f"Cannot perform addition of Point with {type(other)}")
        return Point(self.x + other.x, self.y + other.y)

    def fits_inside(self, other: BoundaryContainer) -> bool:
        return (other.top_left.x <= self.x <= other.bottom_right.x
                and other.top_left.y <= self.y <= other.bottom_right.y)
