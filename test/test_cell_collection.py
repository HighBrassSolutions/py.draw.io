import pytest

from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.cell import Cell
from py_draw_io.cell_collection import CellCollection, CellNotFoundError, IllegalBoundaryError
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.point import Point
from test.helpers import DummyBoundaryContainer


def test_to_string():
    data = CellCollection()

    assert "0" in str(data)
    assert str(data) == repr(data)

    cell = Cell("test_cell", None, "", None)
    data = CellCollection([cell])
    assert "1" in str(data)
    assert str(data) == repr(data)


def test_append():
    cell = Cell("test_cell", None, "", None)
    data = CellCollection()

    assert len(data) == 0
    data.append(cell)
    assert len(data) == 1


def test_constructor():
    cell = Cell("test_cell", None, "", None)

    assert len(CellCollection()) == 0
    assert len(CellCollection([])) == 0
    assert len(CellCollection([cell])) == 1


def test_length():
    base_cell_1 = Cell("bc1", None, "", None)
    base_cell_2 = Cell("bc2", None, "", None)
    base_cell_3 = Cell("bc3", None, "", None)
    child_cell_1 = Cell("bc1", None, "", base_cell_1)
    _ = Cell("bc1", None, "", base_cell_1)
    _ = Cell("bc1", None, "", child_cell_1)

    assert len(CellCollection([base_cell_1, base_cell_2, base_cell_3])) == 6
    assert len(CellCollection([base_cell_1])) == 4
    assert len(CellCollection([base_cell_2, base_cell_3])) == 2


def test_find_by_id():
    base_cell_1 = Cell("bc1", None, "", None)
    base_cell_2 = Cell("bc2", None, "", None)
    base_cell_3 = Cell("bc3", None, "", None)
    child_cell_1 = Cell("cc1", None, "", base_cell_1)
    child_cell_2 = Cell("cc2", None, "", base_cell_1)
    grandchild_cell_1 = Cell("gc1", None, "", child_cell_1)
    collection = CellCollection([base_cell_1, base_cell_2, base_cell_3])

    assert collection.find_by_id("bc1") == base_cell_1
    assert collection.find_by_id("bc2") == base_cell_2
    assert collection.find_by_id("bc3") == base_cell_3
    assert collection.find_by_id("cc1") == child_cell_1
    assert collection.find_by_id("cc2") == child_cell_2
    assert collection.find_by_id("gc1") == grandchild_cell_1

    with pytest.raises(CellNotFoundError):
        collection.find_by_id("not_existent")


def test_remove_cells_outside_boundary():
    c1 = GeometryCell("c1", None, "", None, Point(10, 10), Point(14, 14))
    c2 = GeometryCell("c2", None, "", None, Point(0, 4), Point(7, 12))
    c3 = GeometryCell("c3", None, "", None, Point(50, 40), Point(55, 55))
    c4 = GeometryCell("c4", None, "", c3, Point(34, 23), Point(36, 43))

    collection = CellCollection([c1, c2, c3])

    collection.remove_cells_outside_boundary(DummyBoundaryContainer(Point(0, 0), Point(45, 45)))

    assert len(collection) == 2

    assert collection.find_by_id("c1")
    assert collection.find_by_id("c2")

    with pytest.raises(CellNotFoundError):
        collection.find_by_id("c3")
    with pytest.raises(CellNotFoundError):
        collection.find_by_id("c4")


def test_remove_cells_outside_boundary_by_id():
    c1 = GeometryCell("c1", None, "", None, Point(55, 67), Point(86, 90))
    c2 = GeometryCell("c2", None, "", None, Point(0, 4), Point(34, 55))
    c3 = GeometryCell("c3", None, "", None, Point(14, 15), Point(18, 19))
    a1 = ArrowCell("a1", None, "", None, c1, c2, [])
    a2 = ArrowCell("a2", None, "", None, c2, c3, [])

    collection = CellCollection([c1, c2, c3, a1, a2])

    with pytest.raises(CellNotFoundError):
        collection.remove_cells_outside_boundary("not_existent")

    with pytest.raises(IllegalBoundaryError):
        collection.remove_cells_outside_boundary("a1")

    collection.remove_cells_outside_boundary("c2")

    assert len(collection) == 3
    assert c2 in collection
    assert c3 in collection
    assert a2 in collection
