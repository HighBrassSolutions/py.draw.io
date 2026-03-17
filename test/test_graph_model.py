from bs4 import BeautifulSoup

from py_draw_io.graph_model import GraphModel


def test_to_string():
    model = GraphModel(10, 400, 600)
    assert "10" in str(model)
    assert "400" in str(model)
    assert "600" in str(model)
    assert str(model) == repr(model)


def test_to_xml():
    model = GraphModel(10, 400, 600)
    xml = model.to_xml()
    assert xml.attrs["gridSize"] == "10"
    assert xml.attrs["pageWidth"] == "400"
    assert xml.attrs["pageHeight"] == "600"


def test_from_xml():
    data = BeautifulSoup("""
        <mxGraphModel dx="364" dy="269" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
        </mxGraphModel>
    """, "xml").find("mxGraphModel")

    model = GraphModel.from_xml(data)
    assert model.grid_size == 10
    assert model.page_width == 827
    assert model.page_height == 1169
