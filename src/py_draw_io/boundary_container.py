from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_draw_io.point import Point


class BoundaryContainer:
    top_left: Point
    bottom_right: Point
