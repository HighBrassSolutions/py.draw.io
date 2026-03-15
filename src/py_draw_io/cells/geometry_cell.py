from __future__ import annotations
from typing import Any, Optional, Dict, Union
from bs4 import Tag
from typing import TYPE_CHECKING

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.errors import XmlDecodingError
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute
from py_draw_io.point import Point
from py_draw_io.cells.cell import Cell

if TYPE_CHECKING:
    from py_draw_io.cell_collection import CellCollection


class GeometryCell(Cell, BoundaryContainer):
    top_left: Point
    bottom_right: Point

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]], value: Optional[str],
                 parent: Optional[Cell], top_left: Point, bottom_right: Point):
        super().__init__(cell_id, style, value, parent)
        if top_left.x > bottom_right.x:
            raise ValueError("Top left point must be smaller than bottom right point")
        if top_left.y > bottom_right.y:
            raise ValueError("Top left point must be smaller than bottom right point")
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.contains_geometry = True

    def __repr__(self):
        return f"GeometryCell({self.id})[{self.top_left}/{self.bottom_right}]"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GeometryCell):
            raise TypeError(f"Cannot compare geometry with {type(other)}")
        return self.top_left == other.top_left and self.bottom_right == other.bottom_right

    @property
    def width(self) -> float:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> float:
        return self.bottom_right.y - self.top_left.y

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    def fits_inside(self, other: BoundaryContainer) -> bool:
        return self.top_left.fits_inside(other) and self.bottom_right.fits_inside(other)

    def to_xml(self) -> Tag:
        base = super().to_xml()
        base.attrs["vertex"] = "1"

        x = self.top_left.x
        if isinstance(self.parent, GeometryCell):
            x -= self.parent.top_left.x

        y = self.top_left.y
        if isinstance(self.parent, GeometryCell):
            y -= self.parent.top_left.y

        out = Tag(name="mxGeometry")
        out.attrs["height"] = str(self.height)
        out.attrs["width"] = str(self.width)
        out.attrs["x"] = str(x)
        out.attrs["y"] = str(y)
        out.attrs["as"] = "geometry"
        base.append(out)
        return base

    @classmethod
    def from_xml(cls, data: Tag, existing_cells: CellCollection) -> GeometryCell:
        cell_id = get_string_attribute(data, "id")
        parent = cls._decode_parent(data, existing_cells)
        style = cls._decode_style(data)
        value = get_optional_string_attribute(data, "value")

        geometry_data = data.find_all("mxGeometry")
        if len(geometry_data) > 1:
            raise XmlDecodingError("Found more than one geometry")
        elif len(geometry_data) == 0:
            raise XmlDecodingError("Found no geometry data")

        geometry_tag = geometry_data[0]
        if "vertex" not in data.attrs:
            raise XmlDecodingError("Geometry is no Geometry")

        x = float(get_string_attribute(geometry_tag,"x", "0"))
        if parent is not None and isinstance(parent, GeometryCell):
            x += parent.top_left.x

        y = float(get_string_attribute(geometry_tag,"y", "0"))
        if parent is not None and isinstance(parent, GeometryCell):
            y += parent.top_left.y

        top_left = Point(x, y)
        bottom_right = Point(top_left.x + float(get_string_attribute(data, "width")),
                             top_left.y + float(get_string_attribute(data, "height")))

        out = GeometryCell(cell_id, style, value, parent, top_left, bottom_right)

        if parent is not None:
            parent.children.append(out)
        return out
