from py_draw_io.cell import Cell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from test.helpers import DummyBoundaryContainer


def test_to_string():
    cell = Cell("test_cell", None, "", None)
    assert "test_cell" in str(cell)
    assert repr(cell) == str(cell)


def test_fits_inside():
    cell = Cell("test_cell", None, "", None)
    assert cell.fits_inside(DummyBoundaryContainer(Point(0, 0), Point(0, 0))) is True


def test_parent_setting():
    """Test the parent/children-attributes get set correctly"""

    layer = Layer(CellCollection(), "1")
    parent = Cell("parent_cell", None, "", layer)
    cell = Cell("test_cell", None, "", parent)
    assert cell.parent == parent
    assert parent.children == [cell]
    assert layer.cells[0] == parent
    assert cell.parent_layer == layer
    assert parent.parent_layer == layer
