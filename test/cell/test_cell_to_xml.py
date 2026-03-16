from py_draw_io.cell import Cell


def test_parent_encoding():
    """Tests the correct encoding of the parent attribute."""

    parent = Cell("parent_cell", {}, "", None)
    cell = Cell("test_cell", {}, "", parent)

    data = cell.to_xml()
    assert data.attrs["parent"] == "parent_cell"

    cell = Cell("test_cell", {}, "", None)
    data = cell.to_xml()
    assert "parent" not in data.attrs


def test_style_encoding():
    """Tests the correct encoding of the parent attribute."""

    cell = Cell("test_cell", {}, "", None)
    data = cell.to_xml()
    assert data.attrs["style"] == ""

    cell = Cell("test_cell", None, "", None)
    data = cell.to_xml()
    assert "style" not in data.attrs

    cell = Cell("test_cell",
                {
                    "int_attr": 12,
                    "str_attr": "yolo",
                    "none_attr": None
                },
                "", None)
    data = cell.to_xml()
    assert data.attrs["style"] == "int_attr=12;str_attr=yolo;none_attr=none"

    cell = Cell("test_cell",
                {
                    "int_attr": 12,
                    "geometry_type": "testerino"
                },
                "", None)
    data = cell.to_xml()
    assert data.attrs["style"] == "testerino;int_attr=12"
