from py_draw_io.cells.arrow_cell import ArrowCell
from py_draw_io.point import Point


def test_edge_property_set():
    """Tests the correct decoding of the parent attribute and the linking between the two objects"""

    arrow = ArrowCell("parent123", {}, "", None, Point(1, 2), Point(4, 5), [])

    data = arrow.to_xml()
    assert data.attrs["edge"] == "1"
