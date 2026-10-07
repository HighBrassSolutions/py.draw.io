from py_draw_io.cell_collection import CellCollection
from py_draw_io.layer import Layer
from test.cell import DummyCell


def test_to_string():
    """Test the string representation"""

    layer = Layer(CellCollection(), "msg", "12name")
    assert "msg" in str(layer)
    assert "12name" in str(layer)
    assert "0 cells" in str(layer)
    assert repr(layer) == str(layer)
    _ = DummyCell("yolo", {}, None, layer)
    assert "1 cells" in str(layer)


def test_to_xml():
    """Test the XML serialization"""

    layer = Layer(CellCollection(), "msg")
    xml = layer.to_xml("blub")

    assert xml.attrs["id"] == "msg"
    assert xml.attrs["parent"] == "blub"
    assert "value" not in xml.attrs

    layer = Layer(CellCollection(), "msg2", "name123")
    xml = layer.to_xml("22")

    assert xml.attrs["id"] == "msg2"
    assert xml.attrs["parent"] == "22"
    assert xml.attrs["value"] == "name123"
