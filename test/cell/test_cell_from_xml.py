import pytest
from bs4 import BeautifulSoup

from py_draw_io.cell import Cell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.errors import XmlDecodingError
from py_draw_io.layer import Layer


def test_decode_style_success():
    """Test the proper decoding of the style attribute"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="rounded=1;whiteSpace=wrap;html=none;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.style["geometry_type"] is None
    assert cell.style["rounded"] == 1
    assert cell.style["whiteSpace"] == "wrap"
    assert cell.style["html"] is None

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="yolo;rounded=1;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.style["geometry_type"] == "yolo"
    assert cell.style["rounded"] == 1


def test_decode_style_illegal_style_string():
    """Test the behavior if the style string is broken"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="rounded=1=2;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError):
        _ = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="rounded=2;test=;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.style["test"] == ""


def test_decode_style_two_geometry_types():
    """Test the raising of an error if two geometry types are set"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="yolo;blub;rounded=1;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError):
        _ = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])


def test_decode_style_missing_attr():
    """Test having no style set if the argument is missing"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.style is None


def test_parent_mapping():
    """Tests the correct decoding of the parent attribute and the linking between the two objects"""
    base_layer = Layer(CellCollection(), "test_layer", None)

    parent = Cell("parent123", {}, "", base_layer)
    assert parent.children == []

    data = BeautifulSoup("""
        <mxCell id="test1" parent="parent123" edge="1" style="">

        </mxCell>
    """, "xml").find("mxCell")

    arrow = Cell.from_xml(data, CellCollection([parent]), [base_layer])

    assert id(arrow.parent) == id(parent)
    assert [id(x) for x in parent.children] == [id(arrow)]


def test_attribute_value():
    """Test the decoding of the value attribute"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="rounded=1;whiteSpace=wrap;html=none;" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.value is None

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="rounded=1;whiteSpace=wrap;html=none;" value="yolo" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    cell = Cell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.value == "yolo"
