"""Module for the Cell class."""
from __future__ import annotations
import copy
from typing import Optional, Union, List, Dict
from bs4 import Tag
from typing import TYPE_CHECKING

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.errors import XmlDecodingError
from py_draw_io.fittable import Fittable
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute

if TYPE_CHECKING:
    from py_draw_io.cell_collection import CellCollection
    from py_draw_io.layer import Layer


class Cell(Fittable):
    """Represents a basic cell with no geometry and also works as parent class for all cells containing geometries."""

    id: str
    style: Optional[Dict[str, Union[int, str, None]]]
    value: Optional[str]
    parent: Union[Cell, Layer]
    children: List[Cell]
    contains_geometry: bool

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]],
                 value: Optional[str], parent: Union[Cell, Layer]):
        """
        Create a new instance of the Cell class.

        :param cell_id: ID of the cell
        :param style: Styling information for the cell
        :param value: Content of the cells text field
        :param parent: Parent cell (if there is one)
        """
        self.id = cell_id
        self.style = style
        self.value = value

        self.parent = parent
        if self.parent is not None:
            if isinstance(self.parent, Cell):
                self.parent.children.append(self)
            else:
                self.parent.cells.append(self)

        self.children = []
        self.contains_geometry = False

    def __repr__(self) -> str:
        return f"BasicCell {self.id}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
        return True

    @property
    def parent_layer(self) -> Layer:
        """The layer this cell is part of."""

        parent = self.parent
        while isinstance(parent, Cell):
            parent = parent.parent
        return parent

    @classmethod
    def _encode_style(cls, style: Dict[str, Union[int, str, None]]) -> str:
        buf = copy.deepcopy(style)
        geo_type = buf.pop("geometry_type", None)
        if geo_type is not None:
            out = f"{geo_type};"
        else:
            out = ""
        for key, value in buf.items():
            if value is None:
                buf[key] = "none"

        out += ";".join([f"{key}={value}" for key, value in buf.items()])
        return out

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        :return: The created XML tag
        """
        out = Tag(name="mxCell")
        out.attrs["id"] = self.id
        if self.parent is not None:
            out.attrs["parent"] = self.parent.id
        if self.value is not None:
            out.attrs["value"] = self.value
        if self.style is not None:
            out.attrs["style"] = self._encode_style(self.style)
        return out

    @classmethod
    def _decode_style(cls, data: Tag) -> Optional[Dict[str, Union[int, str, None]]]:
        if "style" not in data.attrs:
            return None

        value = get_string_attribute(data, "style")

        parts = [x.split("=") for x in value.strip(";").split(";")]
        style = {}
        keywords = [x for x in parts if len(x) == 1]
        pairs = [x for x in parts if len(x) == 2]
        if len(pairs) + len(keywords) != len(parts):
            raise XmlDecodingError("Illegal style string detected")
        if len(keywords) > 1:
            raise XmlDecodingError("More than one keyword detected")
        for key, raw_value in pairs:
            final_value: Union[int, str, None] = raw_value
            try:
                final_value = int(raw_value)
            except ValueError:
                pass
            if raw_value == "none":
                final_value = None
            style[key] = final_value
        if keywords:
            style["geometry_type"] = keywords[0][0]
        else:
            style["geometry_type"] = None
        return style

    @classmethod
    def _decode_parent(cls, data: Tag, existing_cells: CellCollection, layers: List[Layer]) -> Union[Cell, Layer]:
        if "parent" not in data.attrs:
            raise XmlDecodingError("No parent tag found")
        parent_id = get_string_attribute(data, "parent")
        for layer in layers:
            if layer.id == parent_id:
                return layer
        return existing_cells.find_by_id(parent_id)

    @classmethod
    def from_xml(cls, data: Tag, existing_cells: CellCollection, layers: List[Layer]) -> Cell:
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

        out = Cell(cell_id, style, value, parent)
        return out
