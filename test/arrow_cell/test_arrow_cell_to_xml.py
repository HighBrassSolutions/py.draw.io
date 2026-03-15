from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.point import Point


def test_edge_property_set():
    """Tests the correct encoding of the 'edge' attribute"""

    arrow = ArrowCell("parent123", {}, "", None, Point(1, 2), Point(4, 5), [])
    data = arrow.to_xml()

    assert data.attrs["edge"] == "1"


def test_relative_property_set():
    """Tests the correct encoding of the 'relative' attribute"""

    arrow = ArrowCell("parent123", {}, "", None, Point(1, 2), Point(4, 5), [])
    data = arrow.to_xml()
    geometry_tag = data.find_all("mxGeometry")[0]

    assert geometry_tag.attrs["relative"] == "1"


def test_point_source():
    """Tests the correct encoding of a Point-source"""

    target = GeometryCell("target_cell", {}, "", None, Point(0, 0), Point(5, 5))
    source = Point(1, 2)
    arrow = ArrowCell("test_cell", {}, "", None, source, target, [])
    data = arrow.to_xml()

    assert "source" not in data.attrs
    points = data.find_all("mxPoint")
    assert len(points) == 1
    assert points[0].attrs["as"] == "sourcePoint"


def test_point_target():
    """Tests the correct encoding of a Point-target"""

    target = Point(1, 2)
    source = GeometryCell("source_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arrow = ArrowCell("test_cell", {}, "", None, source, target, [])
    data = arrow.to_xml()

    assert "target" not in data.attrs
    points = data.find_all("mxPoint")
    assert len(points) == 1
    assert points[0].attrs["as"] == "targetPoint"


def test_cell_source():
    """Tests the correct encoding of a Cell-source"""

    target = Point(1, 2)
    source = GeometryCell("source_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arrow = ArrowCell("test_cell", {}, "", None, source, target, [])
    data = arrow.to_xml()

    assert data.attrs["source"] == "source_cell"
    points = data.find_all("mxPoint")
    assert len(points) == 1
    assert points[0].attrs["as"] != "sourcePoint"


def test_cell_target():
    """Tests the correct encoding of a Cell-target"""

    target = GeometryCell("target_cell", {}, "", None, Point(0, 0), Point(5, 5))
    source = Point(1, 2)
    arrow = ArrowCell("test_cell", {}, "", None, source, target, [])
    data = arrow.to_xml()

    assert data.attrs["target"] == "target_cell"
    points = data.find_all("mxPoint")
    assert len(points) == 1
    assert points[0].attrs["as"] != "targetPoint"


def test_waypoints():
    """Tests the correct encoding of a Cell-target"""

    target = GeometryCell("target_cell", {}, "", None, Point(0, 0), Point(5, 5))
    source = GeometryCell("source_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arrow = ArrowCell("test_cell", {}, "", None, source, target, [])
    data = arrow.to_xml()

    points = data.find_all("mxPoint")
    assert len(points) == 0

    arrow = ArrowCell("test_cell", {}, "", None, source, target,
                      [Point(100, 200)])
    data = arrow.to_xml()

    points = data.find_all("mxPoint")
    assert len(points) == 1
    point = points[0]
    assert "as" not in point.attrs
    assert point.attrs["x"] == "100"
    assert point.attrs["y"] == "200"
