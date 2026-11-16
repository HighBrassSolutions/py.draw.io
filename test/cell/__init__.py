"""Tests for the Cell class."""
from bs4 import Tag

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.cell import Cell
from py_draw_io.cell_collection import CellCollection
from py_draw_io.helpers import get_optional_string_attribute, get_string_attribute
from py_draw_io.layer import Layer


class DummyCell(Cell):
    def fits_inside(self, other: BoundaryContainer) -> bool:  # noqa: ARG002 (must match Fittable's signature)
        return True

    @classmethod
    def from_xml(cls, data: Tag, existing_cells: CellCollection, layers: list[Layer]) -> Cell:
        """
        Create a Cell from the given xml data.

        :param data: XML tag to create the Cell from
        :param existing_cells: Cells already parsed from the XML document
        :param layers: Layers parsed from the XML document
        :return: The created Cell
        :raises XmlDecodingError: If any of the required attributes is missing
        """
        cell_id = get_string_attribute(data, "id")
        parent = cls._decode_parent(data, existing_cells, layers)
        style = cls._decode_style(data)
        value = get_optional_string_attribute(data, "value")

        return DummyCell(cell_id, style, value, parent)
