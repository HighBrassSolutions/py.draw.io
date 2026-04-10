"""Module for the Diagram class."""
from __future__ import annotations
from typing import List
from bs4 import Tag

from py_draw_io.cell import Cell
from .cell_collection import CellCollection, CellNotFoundError
from py_draw_io.arrow_cell import ArrowCell
from py_draw_io.geometry_cell import GeometryCell
from .errors import XmlDecodingError
from .graph_model import GraphModel
from .helpers import get_string_attribute
from .layer import Layer


class Diagram:
    """Represents a draw.io diagram with all its geometries and arrows."""

    name: str
    id: str
    layers: List[Layer]
    graph_model: GraphModel

    def __init__(self, name: str, diagram_id: str, layers: List[Layer], graph_model: GraphModel) -> None:
        """
        Create a new instance of the Diagram class.

        :param name: Name of the diagram
        :param diagram_id: ID of the diagram
        :param layers: Layers with Cells containing the diagrams geometries
        :param graph_model: Graph model for the diagram
        """
        self.name = name
        self.id = diagram_id
        self.layers = layers
        self.graph_model = graph_model

    def __repr__(self) -> str:
        return f"Diagram({self.name}, {self.id}, {len(self.layers)} layers)"

    def find_by_id(self, cell_id: str) -> Cell:
        """
        Search the diagram for a cell with the given id recursively.

        :param cell_id: ID to find a matching cell for
        :raises CellNotFoundError: If no cell was found for the given ID
        :return: The cell if one was found
        """
        for layer in self.layers:
            try:
                return layer.cells.find_by_id(cell_id)
            except CellNotFoundError:
                pass
        raise CellNotFoundError(cell_id)

    @classmethod
    def _build_cell(cls, data: Tag, existing_cells: CellCollection, layers: List[Layer]) -> Cell:
        """Create a fitting cell object from the given XML tag."""
        try:
            return ArrowCell.from_xml(data, existing_cells, layers)
        except XmlDecodingError:
            pass
        try:
            return GeometryCell.from_xml(data, existing_cells, layers)
        except XmlDecodingError:
            pass
        return Cell.from_xml(data, existing_cells, layers)

    @classmethod
    def _build_cells(cls, xml_cells: List[Tag], existing_cells: CellCollection, layers: List[Layer]) -> None:
        """
        Create a list of cells from the given XML tags.

        Recursively tries again should one cells parent not be available during creation.
        """
        failed_to_build = []
        for cell_data in xml_cells:
            try:
                existing_cells.append(cls._build_cell(cell_data, existing_cells, layers))
            except CellNotFoundError:
                failed_to_build.append(cell_data)

        if len(failed_to_build) != 0:
            if len(failed_to_build) == len(xml_cells):
                raise XmlDecodingError(f"{len(failed_to_build)} cells could not be properly connected to their parent")
            cls._build_cells(failed_to_build, existing_cells, layers)

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        :return: The created XML tag
        """

        def build_cells(cells: List[Cell]) -> List[Tag]:
            out_tags = []
            for cell_data in cells:
                out_tags.append(cell_data.to_xml())
                out_tags += build_cells(cell_data.children)
            return out_tags

        out = Tag(name="diagram")
        out.attrs["id"] = self.id
        out.attrs["name"] = self.name
        graph_model = self.graph_model.to_xml()
        root = Tag(name="root")

        base_cell = Tag(name="mxCell")
        base_cell.attrs["id"] = "0"
        root.append(base_cell)

        for layer in self.layers:
            root.append(layer.to_xml())
            for cell_tag in build_cells(list(layer.cells)):
                root.append(cell_tag)

        graph_model.append(root)
        out.append(graph_model)
        return out

    @classmethod
    def from_xml(cls, data: Tag) -> Diagram:
        """
        Create a Diagram from the given XML data.

        :param data: XML tag to create the Diagram from
        :return: The created Diagram
        :raises XmlDecodingError: If any of the required attributes is missing
        """
        model_data = data.find_all("mxGraphModel")
        if len(model_data) != 1:
            raise XmlDecodingError("found more or less than one model data")
        model = GraphModel.from_xml(model_data[0])
        cells = CellCollection()
        xml_cells: List[Tag] = data.find_all("mxCell")

        base_cells = [x for x in xml_cells if "parent" not in x.attrs]
        if len(base_cells) != 1:
            raise XmlDecodingError(f"Found {len(base_cells)} base cells, must be exactly 1")
        base_cell_id = base_cells[0].attrs["id"]

        layer_cells = [x for x in xml_cells if "parent" in x.attrs and x.attrs["parent"] == base_cell_id]
        layers = [Layer.from_xml(x) for x in layer_cells]

        xml_cells = [x for x in xml_cells if x not in base_cells + layer_cells]

        cls._build_cells(xml_cells, cells, layers)

        return cls(get_string_attribute(data, "name"), get_string_attribute(data, "id"), layers, model)
