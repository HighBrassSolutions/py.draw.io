import pytest

from py_draw_io.cell_collection import CellCollection
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.layer import Layer
from py_draw_io.point import Point


def test_to_string():
    """Tests the string representation of the geometry cell."""

    layer = Layer(CellCollection(), "1")
    g = GeometryCell("33test99", {}, "", layer, Point(12, 55), Point(44, 77))
    assert "33test99" in str(g)
    assert "12" in str(g)
    assert "55" in str(g)
    assert "44" in str(g)
    assert "77" in str(g)
    assert repr(g) == str(g)


def test_height():
    """Tests the height calculation"""

    layer = Layer(CellCollection(), "1")
    g = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(55, 65))
    assert g.height == 55


def test_width():
    """Tests the width calculation"""

    layer = Layer(CellCollection(), "1")
    g = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(55, 65))
    assert g.width == 45


def test_aspect_ratio():
    """Tests the aspect ratio calculation"""

    layer = Layer(CellCollection(), "1")
    g = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(40, 40))
    assert g.aspect_ratio == 1

    g = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(40, 70))
    assert g.aspect_ratio == 0.5

    g = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(70, 40))
    assert g.aspect_ratio == 2


def test_constructor():
    """Tests that the constructor recognizes illegal points"""
    layer = Layer(CellCollection(), "1")
    _ = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(10, 10))

    with pytest.raises(ValueError):
        _ = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(9, 10))

    with pytest.raises(ValueError):
        _ = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(10, 9))

    with pytest.raises(ValueError):
        _ = GeometryCell("33test99", {}, "", layer, Point(10, 10), Point(9, 9))
