from bs4 import Tag, BeautifulSoup

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.point import Point


class DummyBoundaryContainer(BoundaryContainer):
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right


def create_tag(xml: str, tag_name: str) -> Tag:
    soup = BeautifulSoup(xml, "xml")
    tag = soup.find(tag_name)
    if not isinstance(tag, Tag):
        raise ValueError()
    return tag
