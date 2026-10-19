from py_draw_io.cell_collection import CellCollection
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from test.cell import DummyCell
from test.helpers import DummyBoundaryContainer


def test_to_string():
    layer = Layer(CellCollection(), "1")
    cell = DummyCell("test_cell", None, "", layer)
    assert "test_cell" in str(cell)
    assert repr(cell) == str(cell)


def test_fits_inside():
    layer = Layer(CellCollection(), "1")
    cell = DummyCell("test_cell", None, "", layer)
    assert cell.fits_inside(DummyBoundaryContainer(Point(0, 0), Point(0, 0))) is True


def test_parent_setting():
    """Test the parent/children-attributes get set correctly"""

    layer = Layer(CellCollection(), "1")
    parent = DummyCell("parent_cell", None, "", layer)
    cell = DummyCell("test_cell", None, "", parent)
    assert cell.parent == parent
    assert parent.children == [cell]
    assert layer.cells[0] == parent
    assert cell.parent_layer == layer
    assert parent.parent_layer == layer
