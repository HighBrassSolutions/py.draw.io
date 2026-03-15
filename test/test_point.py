import pytest

from py_draw_io.point import Point
from test.helpers import DummyBoundaryContainer


def test_to_string():
    """Test the string representation"""

    p = Point(12, 55)
    assert "12" in str(p)
    assert "55" in str(p)
    assert repr(p) == str(p)


def test_equals():
    """Tests the equality operator"""

    p = Point(12, 55)

    with pytest.raises(TypeError):
        _ = p == 2

    assert p == Point(12, 55)
    assert p == p
    assert p != Point(13, 55)
    assert p != Point(12, 56)


def test_add():
    """Tests the addition operator"""

    p = Point(12, 55)

    with pytest.raises(TypeError):
        _ = p + 2
    assert p + Point(1, 1) == Point(13, 56)
    assert p + Point(-1, -1) == Point(11, 54)
    assert p + Point(1, -1) == Point(13, 54)


def test_fits_inside():
    """Tests the fits_inside method"""

    p = Point(12, 55)
    assert p.fits_inside(DummyBoundaryContainer(Point(1, 1), p))
    assert p.fits_inside(DummyBoundaryContainer(p, Point(200, 200)))
    assert p.fits_inside(DummyBoundaryContainer(p, p))
    assert p.fits_inside(DummyBoundaryContainer(Point(12, 44),
                                                Point(44, 55)))
    assert p.fits_inside(DummyBoundaryContainer(Point(4, 55),
                                                Point(12, 67)))

    assert not p.fits_inside(DummyBoundaryContainer(Point(13, 56),
                                                    Point(200, 200)))
