import pytest

from py_draw_io.cells.arrow_cell import ArrowCell
from py_draw_io.point import Point


def test_to_string():
    """Tests the string representation"""

    arrow = ArrowCell("12test55", {}, "", None, Point(30, 55), Point(60, 77), [])

    assert str(arrow).count(" -> ") == 1
    assert "12test55" in str(arrow)
    assert "30" in str(arrow)
    assert "55" in str(arrow)
    assert "60" in str(arrow)
    assert "77" in str(arrow)
    assert repr(arrow) == str(arrow)

    arrow2 = ArrowCell("12test55", {}, "", None, Point(30, 55), Point(60, 77), [Point(33, 44)])
    assert str(arrow2).count(" -> ") == 2


def test_equals():
    """Tests the equality comparison"""

    arrow = ArrowCell("12test55", {}, "", None,
                      Point(30, 55),
                      Point(60, 77),
                      [Point(11, 12)])

    with pytest.raises(TypeError):
        _ = arrow == 2

    assert arrow == arrow

    # waypoints make a difference when comparing
    assert arrow != ArrowCell("12test55", {}, "", None,
                              Point(30, 55),
                              Point(60, 77),
                              [Point(10, 12)])

    assert arrow != ArrowCell("12test55", {}, "", None,
                              Point(30, 55),
                              Point(60, 77),
                              [Point(10, 12), Point(10, 55)])

    # source makes a difference when comparing
    assert arrow != ArrowCell("12test55", {}, "", None,
                              Point(31, 55),
                              Point(60, 77),
                              [Point(11, 12)])

    # target makes a difference when comparing
    assert arrow != ArrowCell("12test55", {}, "", None,
                              Point(30, 55),
                              Point(61, 77),
                              [Point(11, 12)])

    # ID makes no difference when comparing
    assert arrow == ArrowCell("12test99", {}, "", None,
                              Point(30, 55),
                              Point(60, 77),
                              [Point(11, 12)])
