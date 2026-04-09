"""Module for the Layer class."""
from __future__ import annotations
from typing import Optional
from bs4 import Tag

from py_draw_io.cell_collection import CellCollection
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute


class Layer:
    """Represents a layer containing the geometries within a diagram."""

    cells: CellCollection
    id: str
    name: Optional[str]

    def __init__(self, cells: CellCollection, layer_id: str, name: str = None) -> None:
        """
        Create a new instance of the Layer class.

        :param cells: Cells the layer contains
        :param layer_id: ID of the layer
        :param name: Name of the layer
        """
        self.cells = cells
        self.id = layer_id
        self.name = name

        for cell in self.cells:
            cell.parent = self

    def __repr__(self) -> str:
        return f"Layer({self.name}, {self.id}, {len(self.cells)} cells)"

    def to_xml(self, parent_id: str = "0") -> Tag:
        """
        Create an XML structure representing this class.

        :param parent_id: The parent cell id
        :return: The created XML tag
        """
        out = Tag(name="mxCell")
        out.attrs["id"] = self.id
        out.attrs["parent"] = parent_id
        if self.name is not None:
            out.attrs["value"] = self.name
        return out

    @classmethod
    def from_xml(cls, data: Tag) -> Layer:
        """
        Create a Layer from the given XML data.

        :param data: XML tag to create the Layer from
        :return: The created Cell
        :raises XmlDecodingError: If any of the required attributes is missing
        """
        layer_id = get_string_attribute(data, "id")
        name = get_optional_string_attribute(data, "value")
        out = Layer(CellCollection(), layer_id, name)
        return out
