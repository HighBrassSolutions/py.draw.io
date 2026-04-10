import pytest

from py_draw_io.cell_collection import CellCollection
from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.errors import XmlDecodingError
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from test.helpers import create_tag


def test_missing_source():
    """Test the decoding of a cell with a missing source"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="529.9999999999998" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "no source specified" in str(err.value)


def test_missing_target():
    """Test the decoding of a cell with a missing target"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="529.9999999999998" as="sourcePoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "no target specified" in str(err.value)


def test_existing_cell_as_target():
    """Test the decoding of a cell defined as target"""

    layer = Layer(CellCollection(), "test_layer", None)
    data = create_tag("""
        <mxCell id="test1" edge="1" style="" target="test2" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="500" as="sourcePoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")
    target = GeometryCell("test2", {}, "", layer, Point(30, 55), Point(60, 77))
    arrow = ArrowCell.from_xml(data, CellCollection([target]), [layer])
    assert isinstance(arrow.target, GeometryCell)
    assert arrow.target.id == "test2"


def test_existing_point_as_target():
    """Test the decoding of a point defined as target"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert isinstance(arrow.target, Point)
    assert arrow.target.x == 55
    assert arrow.target.y == 44


def test_existing_cell_as_source():
    """Test the decoding of a cell defined as source"""

    layer = Layer(CellCollection(), "test_layer", None)
    data = create_tag("""
        <mxCell id="test1" edge="1" style="" source="test2" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="440" y="500" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    source = GeometryCell("test2", {}, "", layer, Point(30, 55), Point(60, 77))
    arrow = ArrowCell.from_xml(data, CellCollection([source]), [layer])
    assert isinstance(arrow.source, GeometryCell)
    assert arrow.source.id == "test2"


def test_existing_point_as_source():
    """Test the decoding of a point defined as source"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert isinstance(arrow.source, Point)
    assert arrow.source.x == 22
    assert arrow.source.y == 1


def test_cell_and_point_target():
    """Test the decoding of a cell with one point and one cell both defined as target"""

    layer = Layer(CellCollection(), "test_layer", None)
    data = create_tag("""
        <mxCell id="test1" edge="1" style="" target="test2" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    target = GeometryCell("test2", {}, "", layer, Point(30, 55), Point(60, 77))
    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection([target]), [layer])
    assert "target" in str(err.value)


def test_two_points_as_target():
    """Test the decoding of a cell with two points defined as target"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "target" in str(err.value)


def test_cell_and_point_source():
    """Test the decoding of a cell with one point and one cell both defined as source"""

    layer = Layer(CellCollection(), "test_layer", None)
    data = create_tag("""
        <mxCell id="test1" edge="1" style="" source="test2" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    source = GeometryCell("test2", {}, "", layer, Point(30, 55), Point(60, 77))
    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection([source]), [layer])
    assert "source" in str(err.value)


def test_two_points_as_source():
    """Test the decoding of a cell with two points defined as source"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="55" y="44" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "source" in str(err.value)


def test_illegal_point_type():
    """Tess the decoding of a cell with an illegal point type specified"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
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
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "Illegal point type" in str(err.value)


def test_waypoints():
    """Test the decoding of the waypoints specified for the arrow"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
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
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])

    assert len(arrow.waypoints) == 3
    assert Point(1, 2) in arrow.waypoints
    assert Point(11, 77) in arrow.waypoints
    assert Point(100, 400) in arrow.waypoints


def test_parent_mapping():
    """Test the correct decoding of the parent attribute and the linking between the two objects"""

    layer = Layer(CellCollection(), "test_layer", None)
    parent = ArrowCell("parent123", {}, "", layer, Point(1, 2), Point(4, 5), [])
    assert parent.children == []

    data = create_tag("""
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
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection([parent]), [layer])

    assert id(arrow.parent) == id(parent)
    assert [id(x) for x in parent.children] == [id(arrow)]


def test_property_check_edge():
    """Test the raising of an error if no 'edge' property was found"""

    data = create_tag("""
        <mxCell id="test1" style="" parent="test_layer">
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
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert str(err.value) == "Geometry is no Arrow"


def test_attribute_value():
    """Test the decoding of the value attribute"""

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert arrow.value is None

    data = create_tag("""
        <mxCell id="test1" edge="1" style="" value="yolo" parent="test_layer">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="22" y="1" as="sourcePoint" />
            <mxPoint x="77" y="66" as="targetPoint" />
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    arrow = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert arrow.value == "yolo"


def test_multiple_geometry_tags():
    """Test the raising of an error if multiple geometry tags were found"""

    data = create_tag("""
        <mxCell id="test1" style="" parent="test_layer">
          <mxGeometry relative="1" as="geometry" />
          <mxGeometry relative="1" as="geometry">
          </mxGeometry>
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "more than one geometry" in str(err.value)


def test_no_geometry_tags():
    """Test the raising of an error if no geometry tags were found"""

    data = create_tag("""
        <mxCell id="test1" style="" parent="test_layer">
        </mxCell>
    """, "mxCell")

    with pytest.raises(XmlDecodingError) as err:
        _ = ArrowCell.from_xml(data, CellCollection(), [Layer(CellCollection(), "test_layer", None)])
    assert "no geometry" in str(err.value)
