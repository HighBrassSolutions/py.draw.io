from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from test.helpers import DummyBoundaryContainer


def test_to_string():
    """Tests the string representation"""

    layer = Layer(CellCollection(), "1")
    arrow = ArrowCell("12test55", {}, "", layer, Point(30, 55), Point(60, 77), [])

    assert str(arrow).count(" -> ") == 1
    assert "12test55" in str(arrow)
    assert "30" in str(arrow)
    assert "55" in str(arrow)
    assert "60" in str(arrow)
    assert "77" in str(arrow)
    assert repr(arrow) == str(arrow)

    arrow2 = ArrowCell("12test55", {}, "", layer, Point(30, 55), Point(60, 77), [Point(33, 44)])
    assert str(arrow2).count(" -> ") == 2


def test_fits_inside():
    """Tests the 'fits_inside' method"""

    layer = Layer(CellCollection(), "1")
    arrow = ArrowCell("12test55", {}, "", layer,
                      Point(30, 55),
                      Point(60, 77),
                      [Point(100, 200)])

    geo1 = DummyBoundaryContainer(Point(30, 55), Point(30, 55))
    assert arrow.source.fits_inside(geo1)
    assert not arrow.fits_inside(geo1)

    geo2 = DummyBoundaryContainer(Point(60, 77), Point(60, 77))
    assert arrow.target.fits_inside(geo2)
    assert not arrow.fits_inside(geo2)

    geo3 = DummyBoundaryContainer(Point(30, 55), Point(60, 77))
    assert not arrow.waypoints[0].fits_inside(geo3)
    assert arrow.fits_inside(geo3)
