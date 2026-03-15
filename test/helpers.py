from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.point import Point


class DummyBoundaryContainer(BoundaryContainer):
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
