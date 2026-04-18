from py_draw_io.cell_collection import CellCollection
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.layer import Layer
from py_draw_io.point import Point

PARENT_LAYER = Layer(CellCollection(), "p_layer_11")


def test_vertex_property_set():
    """Test the correct encoding of the 'edge' attribute"""

    geo = GeometryCell("test_cell", {}, "", PARENT_LAYER, Point(1, 2), Point(4, 5))
    data = geo.to_xml()

    assert data.attrs["vertex"] == "1"


def test_geometry_properties_set():
    """Test the correct encoding of the generic geometry attributes"""

    geo = GeometryCell("test_cell", {}, "", PARENT_LAYER, Point(1, 2), Point(4, 5))
    data = geo.to_xml()

    geometries = data.find_all("mxGeometry")
    assert len(geometries) == 1
    xml_geo = geometries[0]

    assert xml_geo.attrs["height"] == str(geo.height)
    assert xml_geo.attrs["width"] == str(geo.width)
    assert xml_geo.attrs["x"] == str(geo.top_left.x)
    assert xml_geo.attrs["y"] == str(geo.top_left.y)
    assert xml_geo.attrs["as"] == "geometry"


def test_relative_parent_coordinates():
    """Test the correct calculation of the coordinates relative to the parent"""

    parent = GeometryCell("parent_cell", {}, "", PARENT_LAYER, Point(10, 10), Point(30, 30))

    geo = GeometryCell("test_cell", {}, "", parent, Point(12, 13), Point(23, 25))
    data = geo.to_xml()

    geometries = data.find_all("mxGeometry")
    assert len(geometries) == 1
    xml_geo = geometries[0]

    assert xml_geo.attrs["height"] == "12"
    assert xml_geo.attrs["width"] == "11"
    assert xml_geo.attrs["x"] == "2"
    assert xml_geo.attrs["y"] == "3"
    assert xml_geo.attrs["as"] == "geometry"
