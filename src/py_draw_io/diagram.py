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


class Diagram:
    """Represents a draw.io diagram with all its geometries and arrows."""

    name: str
    id: str
    cells: CellCollection
    graph_model: GraphModel

    def __init__(self, name: str, diagram_id: str, cells: CellCollection, graph_model: GraphModel) -> None:
        """
        Create a new instance of the Diagram class.

        :param name: Name of the diagram
        :param diagram_id: ID of the diagram
        :param cells: Cells containing the diagrams geometries
        :param graph_model: Graph model for the diagram
        """
        self.name = name
        self.id = diagram_id
        self.cells = cells
        self.graph_model = graph_model

    def __repr__(self) -> str:
        return f"Diagram({self.name}, {self.id}, {len(self.cells)} cells)"

    @classmethod
    def _build_cell(cls, data: Tag, existing_cells: CellCollection) -> Cell:
        """Create a fitting cell object from the given xml tag."""
        try:
            return ArrowCell.from_xml(data, existing_cells)
        except XmlDecodingError:
            pass
        try:
            return GeometryCell.from_xml(data, existing_cells)
        except XmlDecodingError:
            pass
        return Cell.from_xml(data, existing_cells)

    @classmethod
    def _build_cells(cls, xml_cells: List[Tag], existing_cells: CellCollection) -> None:
        """
        Create a list of cells from the given xml tags.

        Recursively tries again should one cells parent not be available during creation.
        """
        failed_to_build = []
        for cell_data in xml_cells:
            try:
                existing_cells.append(cls._build_cell(cell_data, existing_cells))
            except CellNotFoundError:
                failed_to_build.append(cell_data)

        if len(failed_to_build) != 0:
            if len(failed_to_build) == len(xml_cells):
                raise XmlDecodingError(f"{len(failed_to_build)} cells could not be properly connected to their parent")
            cls._build_cells(failed_to_build, existing_cells)

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
        for cell in build_cells(list(self.cells)):
            root.append(cell)
        graph_model.append(root)
        out.append(graph_model)
        return out

    @classmethod
    def from_xml(cls, data: Tag) -> Diagram:
        """
        Create a Diagram from the given xml data.

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
        cls._build_cells(xml_cells, cells)

        root_cells = CellCollection([x for x in cells if x.parent is None])
        return cls(get_string_attribute(data, "name"), get_string_attribute(data, "id"), root_cells, model)
