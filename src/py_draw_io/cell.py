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


class Cell(Fittable):
    id: str
    style: Optional[Dict[str, Union[int, str, None]]]
    value: Optional[str]
    parent: Optional[Cell]
    children: List[Cell]
    contains_geometry: bool

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]],
                 value: Optional[str], parent: Optional[Cell]):
        """
        Constructor for the Cell class.

        :param cell_id: ID of the cell
        :param style: Styling information for the cell
        :param value: Content of the cells text field
        :param parent: Parent cell (if there is one)
        """
        self.id = cell_id
        self.style = style
        self.value = value
        self.parent = parent
        self.children = []
        self.contains_geometry = False

    def __repr__(self) -> str:
        return f"BasicCell {self.id}"

    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
        return True

    def _encode_style(self) -> str:
        if self.style is None:
            return ""
        buf = copy.deepcopy(self.style)
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
        out = Tag(name="mxCell")
        out.attrs["id"] = self.id
        if self.parent is not None:
            out.attrs["parent"] = self.parent.id
        if self.value is not None:
            out.attrs["value"] = self.value
        if self.style is not None:
            out.attrs["style"] = self._encode_style()
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
    def _decode_parent(cls, data: Tag, existing_cells: CellCollection) -> Optional[Cell]:
        if "parent" not in data.attrs:
            return None
        return [x for x in existing_cells if x.id == data.attrs["parent"]][0]

    @classmethod
    def from_xml(cls, data: Tag, existing_cells: CellCollection) -> Cell:
        """
        Create a Cell from the given xml data.

        :param data: XML tag to create the Cell from
        :param existing_cells: Cells already parsed from the XML document
        :return: The created Cell
        :raises XmlDecodingError: If any of the required attributes is missing
        """
        cell_id = get_string_attribute(data, "id")
        parent = cls._decode_parent(data, existing_cells)
        style = cls._decode_style(data)
        value = get_optional_string_attribute(data, "id")

        out = Cell(cell_id, style, value, parent)

        if parent is not None:
            parent.children.append(out)
        return out
