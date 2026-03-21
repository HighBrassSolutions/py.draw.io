import pytest

from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.diagram import Diagram
from py_draw_io.document import Document, DiagramNotFoundError, NoDrawioDocumentError
from py_draw_io.geometry_cell import GeometryCell
from py_draw_io.graph_model import GraphModel
from py_draw_io.point import Point

DUMMY_DATA = """
<mxfile host="Electron" agent="Testerino" version="29.6.1" pages="3">
  <diagram name="system" id="rMK6Qri9A2ZtsiWg45jE">
    <mxGraphModel dx="2218" dy="1640" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
      </root>
    </mxGraphModel>
  </diagram>
  <diagram id="69C91-wjoXnYqn4PnUJh" name="data">
    <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
      </root>
    </mxGraphModel>
  </diagram>
  <diagram id="R75-8NS8Kljy3cZdzqBM" name="wireframes">
    <mxGraphModel dx="1220" dy="902" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def test_get_document():
    model = GraphModel(10, 400, 600)
    geo1 = GeometryCell("geo_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arr1 = ArrowCell("arrow_cell", {}, "", None, geo1, Point(100, 100), [])
    diagram = Diagram("test_diag", "test_diag_id_123", CellCollection([geo1, arr1]), model)
    diagram2 = Diagram("empty_diag", "empty_diag_id_321", CellCollection(), model)
    doc = Document([diagram, diagram2], "local", "47")

    with pytest.raises(DiagramNotFoundError):
        doc.get_diagram("not_there")

    found = doc.get_diagram("test_diag")
    assert found.id == "test_diag_id_123"

    found = doc.get_diagram("test_diag_id_123")
    assert found.name == "test_diag"


def test_length():
    model = GraphModel(10, 400, 600)
    diagram = Diagram("empty_diag", "empty_diag_id_321", CellCollection(), model)
    diagram2 = Diagram("empty_diag", "empty_diag_id_321", CellCollection(), model)
    doc = Document([diagram, diagram2], "local", "47")

    assert len(doc) == 2


def test_load_success(temp_dir):
    temp_file = temp_dir / "test_file.drawio"
    with open(temp_file, "w") as file_p:
        file_p.write(DUMMY_DATA)

    diagram = Document.load(temp_file)
    assert diagram.host == "Electron"
    assert diagram.agent == "Testerino"
    assert len(diagram) == 3


def test_load_empty_file(temp_dir):
    temp_file = temp_dir / "test_file.drawio"
    with open(temp_file, "w") as file_p:
        file_p.write("")

    with pytest.raises(NoDrawioDocumentError) as err:
        _ = Document.load(temp_file)


def test_load_file_not_found(temp_dir):
    temp_file = temp_dir / "test_file.drawio"

    with pytest.raises(FileNotFoundError):
        _ = Document.load(temp_file)


def test_to_xml(temp_dir):
    temp_file = temp_dir / "test_file.drawio"

    model = GraphModel(10, 400, 600)
    geo1 = GeometryCell("geo_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arr1 = ArrowCell("arrow_cell", {}, "", None, geo1, Point(100, 100), [])
    diagram = Diagram("test_diag", "test_diag_id_123", CellCollection([geo1, arr1]), model)
    diagram2 = Diagram("empty_diag", "empty_diag_id_321", CellCollection(), model)
    doc = Document([diagram, diagram2], "local", "47")

    xml_data = doc.to_xml()
    assert xml_data.attrs["host"] == "local"
    assert xml_data.attrs["agent"] == "47"
    assert xml_data.attrs["pages"] == "2"
    assert len(xml_data) == 2


def test_save(temp_dir):
    temp_file = temp_dir / "test_file.drawio"

    model = GraphModel(10, 400, 600)
    geo1 = GeometryCell("geo_cell", {}, "", None, Point(0, 0), Point(5, 5))
    arr1 = ArrowCell("arrow_cell", {}, "", None, geo1, Point(100, 100), [])
    diagram = Diagram("test_diag", "test_diag_id_123", CellCollection([geo1, arr1]), model)
    diagram2 = Diagram("empty_diag", "empty_diag_id_321", CellCollection(), model)
    doc = Document([diagram, diagram2], "local", "47")

    doc.save(temp_file)
