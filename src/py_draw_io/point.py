"""Module for the Point class."""
from __future__ import annotations

from .boundary_container import BoundaryContainer
from .fittable import Fittable


class Point(Fittable):
    """Represents a point in the diagram."""

    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """
        Create a new instance of the Point class.

        :param x: X-Coordinate in the diagram.
        :param y: Y-Coordinate in the diagram.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            raise TypeError(f"Cannot compare Point with {type(other)}")
        return self.x == other.x and self.y == other.y

    def __add__(self, other: object) -> Point:
        if not isinstance(other, Point):
            raise TypeError(f"Cannot perform addition of Point with {type(other)}")
        return Point(self.x + other.x, self.y + other.y)

    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
        return (other.top_left.x <= self.x <= other.bottom_right.x
                and other.top_left.y <= self.y <= other.bottom_right.y)
