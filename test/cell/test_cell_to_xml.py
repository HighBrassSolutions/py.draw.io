from py_draw_io.cell_collection import CellCollection
from py_draw_io.layer import Layer
from test.cell import DummyCell

PARENT_LAYER = Layer(CellCollection(), "p_layer_11")


def test_parent_encoding():
    """Tests the correct encoding of the parent attribute."""

    parent = DummyCell("parent_cell", {}, "", PARENT_LAYER)
    cell = DummyCell("test_cell", {}, "", parent)

    data = cell.to_xml()
    assert data.attrs["parent"] == "parent_cell"


def test_style_encoding():
    """Tests the correct encoding of the parent attribute."""

    cell = DummyCell("test_cell", {}, "", PARENT_LAYER)
    data = cell.to_xml()
    assert data.attrs["style"] == ""

    cell = DummyCell("test_cell", None, "", PARENT_LAYER)
    data = cell.to_xml()
    assert "style" not in data.attrs

    cell = DummyCell("test_cell",
                     {
                         "int_attr": 12,
                         "str_attr": "yolo",
                         "none_attr": None,
                     },
                     "yolo1", Layer(CellCollection(), "layer1"))
    data = cell.to_xml()
    assert data.attrs["style"] == "int_attr=12;str_attr=yolo;none_attr=none"
    assert data.attrs["value"] == "yolo1"

    cell = DummyCell("test_cell",
                     {
                         "int_attr": 12,
                         "geometry_type": "testerino",
                     },
                     None, Layer(CellCollection(), "layer1"))
    data = cell.to_xml()
    assert data.attrs["style"] == "testerino;int_attr=12"
    assert "value" not in data.attrs
