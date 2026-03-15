import pytest
from bs4 import BeautifulSoup

from py_draw_io.cell_collection import CellCollection
from py_draw_io.cells.arrow_cell import ArrowCell
from py_draw_io.cells.geometry_cell import GeometryCell
from py_draw_io.errors import XmlDecodingError
from py_draw_io.point import Point


def test_missing_source():
    """Tests the decoding of a cell with a missing source"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="529.9999999999998" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "no source specified" in str(err.value)


def test_missing_target():
    """Tests the decoding of a cell with a missing target"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="529.9999999999998" as="sourcePoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "no target specified" in str(err.value)


def test_existing_cell_as_target():
    """Tests the decoding of a cell defined as target"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="" target="test2">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="500" as="sourcePoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")
    target = GeometryCell("test2", "", "", None, Point(30, 55), Point(60, 77))
    arrow = ArrowCell.from_xml(data, CellCollection([target]))
    assert arrow.target.id == "test2"


def test_existing_point_as_target():
    """Tests the decoding of a point defined as target"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection())
    assert arrow.target.x == 55
    assert arrow.target.y == 44


def test_existing_cell_as_source():
    """Tests the decoding of a cell defined as source"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="" source="test2">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="500" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    source = GeometryCell("test2", "", "", None, Point(30, 55), Point(60, 77))
    arrow = ArrowCell.from_xml(data, CellCollection([source]))
    assert arrow.source.id == "test2"


def test_existing_point_as_source():
    """Tests the decoding of a point defined as source"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection())
    assert arrow.source.x == 22
    assert arrow.source.y == 1


def test_cell_and_point_target():
    """Tests the decoding of a cell with one point and one cell both defined as target"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="" target="test2">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    target = GeometryCell("test2", "", "", None, Point(30, 55), Point(60, 77))
    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection([target]))
    assert "target" in str(err.value)


def test_two_points_as_target():
    """Tests the decoding of a cell with two points defined as target"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "target" in str(err.value)


def test_cell_and_point_source():
    """Tests the decoding of a cell with one point and one cell both defined as source"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="" source="test2">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    source = GeometryCell("test2", "", "", None, Point(30, 55), Point(60, 77))
    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection([source]))
    assert "source" in str(err.value)


def test_two_points_as_source():
    """Tests the decoding of a cell with two points defined as source"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "source" in str(err.value)


def test_illegal_point_type():
    """Tess the decoding of a cell with an illegal point type specified"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
            <Array as="points">
                <mxPoint x="387" y="430" />
                <mxPoint x="498" y="430" />
                <mxPoint x="498" y="390" />
            </Array>
            <mxPoint x="55" y="44" as="illegalPoint" />
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "Illegal point type" in str(err.value)


def test_waypoints():
    """Tests the decoding of the waypoints specified for the arrow"""

    data = BeautifulSoup("""
        <mxCell id="test1" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
            <Array as="points">
                <mxPoint x="1" y="2" />
                <mxPoint x="11" y="77" />
                <mxPoint x="100" y="400" />
            </Array>
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection())

    assert len(arrow.waypoints) == 3
    assert Point(1, 2) in arrow.waypoints
    assert Point(11, 77) in arrow.waypoints
    assert Point(100, 400) in arrow.waypoints


def test_parent_mapping():
    """Tests the correct decoding of the parent attribute and the linking between the two objects"""

    parent = ArrowCell("parent123", "", "", None, Point(1, 2), Point(4, 5), [])
    assert parent.children == []

    data = BeautifulSoup("""
        <mxCell id="test1" parent="parent123" edge="1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
            <Array as="points">
                <mxPoint x="1" y="2" />
                <mxPoint x="11" y="77" />
                <mxPoint x="100" y="400" />
            </Array>
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection([parent]))

    assert id(arrow.parent) == id(parent)
    assert [id(x) for x in parent.children] == [id(arrow)]


def test_property_check_edge():
    """Tests the raising of an error if no 'edge' property was found"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
            <Array as="points">
                <mxPoint x="1" y="2" />
                <mxPoint x="11" y="77" />
                <mxPoint x="100" y="400" />
            </Array>
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert str(err.value) == "Geometry is no Arrow"


def test_multiple_geometry_tags():
    """Tests the raising of an error if multiple geometry tags were found"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="">
          <mxGeometry relative="1" as="geometry" />
          <mxGeometry relative="1" as="geometry">
          </mxGeometry>
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "more than one geometry" in str(err.value)


def test_no_geometry_tags():
    """Tests the raising of an error if no geometry tags were found"""

    data = BeautifulSoup("""
        <mxCell id="test1" style="">
        </mxCell>
    """, "xml").find("mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection())
    assert "no geometry" in str(err.value)
