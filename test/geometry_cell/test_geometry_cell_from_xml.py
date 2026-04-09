import pytest
from bs4 import BeautifulSoup

from py_draw_io.cell_collection import CellCollection
from py_draw_io.errors import XmlDecodingError
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.layer import Layer
from py_draw_io.point import Point


def test_missing_attribute_vertex():
    """Test the decoding of a cell with a missing vertex attribute"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" value="" parent="test_layer">
          <mxGeometry height="32.5" width="150" x="311.25" y="358.75" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "Cell is no Geometry" in str(err.value)


def test_missing_geometry():
    """Test the decoding of a cell with a missing geometry tag"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" value="" vertex="1" parent="test_layer">
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "no geometry data" in str(err.value)


def test_multiple_geometries():
    """Test the decoding of a cell with multiple geometry tags"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" value="" vertex="1" parent="test_layer">
        <mxGeometry height="32.5" width="150" x="311.25" y="358.75" as="geometry" />
        <mxGeometry height="32.5" width="150" x="311.25" y="358.75" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "more than one geometry" in str(err.value)


def test_multiple_success():
    """Test the normal decoding of a geometry cell"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" value="" vertex="1" parent="test_layer">
        <mxGeometry height="32.5" width="150" x="300.2" y="400.5" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    cell = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.top_left == Point(300.2, 400.5)
    assert cell.bottom_right == Point(450.2, 433.0)


def test_with_geometry_parent():
    """Test the normal decoding of a geometry cell"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" value="" vertex="1" parent="parent_c">
        <mxGeometry height="2" width="3" x="1" y="4" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    parent = GeometryCell("parent_c", {}, "", None, Point(10, 10), Point(20, 20))

    cell = GeometryCell.from_xml(data, CellCollection([parent]), [Layer(CellCollection(), "test_layer", None)])
    assert cell.top_left == Point(11, 14)
    assert cell.bottom_right == Point(14, 16)


def test_attribute_value():
    """Test the decoding of the value attribute"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="" vertex="1" parent="test_layer">
        <mxGeometry height="32.5" width="150" x="300.2" y="400.5" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    cell = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.value is None

    data = BeautifulSoup("""
        <mxCell id="test1" style="" vertex="1" value="yolo" parent="test_layer">
        <mxGeometry height="32.5" width="150" x="300.2" y="400.5" as="geometry" />
        </mxCell>
    """, "xml").find("mxCell")

    cell = GeometryCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert cell.value == "yolo"
