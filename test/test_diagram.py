import pytest
from bs4 import BeautifulSoup

from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.diagram import Diagram
from py_draw_io.errors import XmlDecodingError
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.graph_model import GraphModel
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from test.helpers import create_tag


def test_to_string():
    model = GraphModel(10, 400, 600)
    diagram = Diagram("test_diag", "diag_id", [], model)
    assert "test_diag" in str(diagram)
    assert "diag_id" in str(diagram)
    assert "0" in str(diagram)
    assert str(diagram) == repr(diagram)


def test_from_xml_success():
    data = create_tag("""
    <diagram id="diag1" name="data">
        <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
          <root>
            <mxCell id="0" />
            <mxCell id="1" parent="0" />
            <mxCell id="arr1" edge="1" parent="1" source="geo1" style="">
              <mxGeometry relative="1" as="geometry">
                <Array as="points">
                  <mxPoint x="330" y="180" />
                  <mxPoint x="330" y="200" />
                </Array>
                <mxPoint x="400" y="280" as="targetPoint" />
              </mxGeometry>
            </mxCell>
            <mxCell id="geo1" parent="1" style="" value="" vertex="1">
              <mxGeometry height="60" width="120" x="140" y="150" as="geometry" />
              <mxPoint x="330" y="180" as="targetPoint"/>
              <mxPoint x="330" y="200" as="sourcePoint"/>
            </mxCell>
            <mxCell id="geo2" parent="1" style="" value="" vertex="1">
              <mxGeometry height="60" width="120" x="450" y="160" as="geometry" />
              <mxPoint x="180" y="330" as="targetPoint"/>
              <mxPoint x="330" y="200" as="sourcePoint"/>
            </mxCell>
          </root>
        </mxGraphModel>
      </diagram>
    """, "diagram")

    diagram = Diagram.from_xml(data)
    assert diagram.id == "diag1"
    assert diagram.name == "data"

    assert diagram.graph_model.grid_size == 10
    assert diagram.graph_model.page_height == 1169
    assert diagram.graph_model.page_width == 827

    assert len(diagram.layers) == 1
    layer = diagram.layers[0]
    assert len(layer.cells) == 3


def test_from_xml_two_graph_models():
    data = create_tag("""
    <diagram id="diag1" name="data">
        <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
        </mxGraphModel>
        <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
        </mxGraphModel>
      </diagram>
    """, "diagram")

    with pytest.raises(XmlDecodingError) as err:
        _ = Diagram.from_xml(data)
    assert "more or less than one model data" in str(err.value)

def test_multiple_base_cells():
    data = create_tag("""
        <diagram id="diag1" name="data">
            <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
              <root>
                <mxCell id="0" />
                <mxCell id="55" />
                <mxCell id="1" parent="0" />
                <mxCell id="geo1" parent="non_existent" style="" value="" vertex="1">
                  <mxGeometry height="60" width="120" x="140" y="150" as="geometry" />
                </mxCell>
                <mxCell id="geo2" parent="1" style=" value="" vertex="1">
                  <mxGeometry height="60" width="120" x="450" y="160" as="geometry" />
                </mxCell>
              </root>
            </mxGraphModel>
          </diagram>
        """, "diagram")

    with pytest.raises(XmlDecodingError) as err:
        _ = Diagram.from_xml(data)
    assert "Found 2 base cells" in str(err.value)

def test_from_xml_no_graph_models():
    data = create_tag("""
    <diagram id="diag1" name="data">
    </diagram>
    """, "diagram")

    with pytest.raises(XmlDecodingError) as err:
        _ = Diagram.from_xml(data)
    assert "more or less than one model data" in str(err.value)


def test_from_xml_missing_reference_cells():
    data = create_tag("""
        <diagram id="diag1" name="data">
            <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
              <root>
                <mxCell id="0" />
                <mxCell id="1" parent="0" />
                <mxCell id="geo1" parent="non_existent" style="" value="" vertex="1">
                  <mxGeometry height="60" width="120" x="140" y="150" as="geometry" />
                </mxCell>
                <mxCell id="geo2" parent="1" style="" value="" vertex="1">
                  <mxGeometry height="60" width="120" x="450" y="160" as="geometry" />
                </mxCell>
              </root>
            </mxGraphModel>
          </diagram>
        """, "diagram")

    with pytest.raises(XmlDecodingError) as err:
        _ = Diagram.from_xml(data)
    assert "cells could not be properly connected to their parent" in str(err.value)


def test_to_xml():
    model = GraphModel(10, 400, 600)
    geo1 = GeometryCell("geo_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arr1 = ArrowCell("arrow_cell", {}, "", None, geo1, Point(100, 100), [])
    layer = Layer(CellCollection([geo1, arr1]), "1")
    diagram = Diagram("test_diag", "diag_id", [layer], model)

    xml_data = diagram.to_xml()
    geometries = xml_data.find_all("mxGeometry")
    assert len(geometries) == 2

    # diags = xml_data.find_all("diagram")
    assert xml_data.name == "diagram"
    assert xml_data.attrs["id"] == "diag_id"
    assert xml_data.attrs["name"] == "test_diag"
