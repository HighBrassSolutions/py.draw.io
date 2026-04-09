"""Module for the GeometryCell."""
from __future__ import annotations
from typing import Optional, Dict, Union, List
from bs4 import Tag
from typing import TYPE_CHECKING

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.errors import XmlDecodingError
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from py_draw_io.cell import Cell

if TYPE_CHECKING:
    from py_draw_io.cell_collection import CellCollection


class GeometryCell(Cell, BoundaryContainer):
    """Represents a cell containing a draw-io geometry."""

    top_left: Point
    bottom_right: Point

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]], value: Optional[str],
                 parent: Union[Cell, Layer], top_left: Point, bottom_right: Point):
        """
        Create a new instance for the ArrowCell class.

        :param cell_id: ID of the cell
        :param style: Styling information for the cell
        :param value: Content of the cells text field
        :param parent: Parent cell (if there is one)
        :param top_left: Top left point of the geometry
        :param bottom_right: Botton right point of the geometry
        """
        super().__init__(cell_id, style, value, parent)
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.contains_geometry = True
        if self.top_left.x > self.bottom_right.x:
            raise ValueError("Top left point must be smaller than bottom right point")
        if self.top_left.y > self.bottom_right.y:
            raise ValueError("Top left point must be smaller than bottom right point")

    def __repr__(self) -> str:
        return f"GeometryCell({self.id})[{self.top_left}/{self.bottom_right}]"

    @property
    def width(self) -> float:
        """The width of the cell."""
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> float:
        """The height of the cell."""
        return self.bottom_right.y - self.top_left.y

    @property
    def aspect_ratio(self) -> float:
        """The aspect ratio of the cell."""
        return self.width / self.height

    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
        return self.top_left.fits_inside(other) and self.bottom_right.fits_inside(other)

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        :return: The created XML tag
        """
        base = super().to_xml()
        base.attrs["vertex"] = "1"

        x = self.top_left.x
        y = self.top_left.y
        if isinstance(self.parent, GeometryCell):
            x -= self.parent.top_left.x
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
    def from_xml(cls, data: Tag, existing_cells: CellCollection, layers: List[Layer]) -> GeometryCell:
        """
        Create a GeometryCell from the given xml data.

        :param data: XML tag to create the GeometryCell from
        :param existing_cells: Cells already parsed from the XML document
        :param layers: Layers parsed from the XML document
        :return: The created GeometryCell
        :raises XmlDecodingError: If any of the required attributes is missing
        """
        cell_id = get_string_attribute(data, "id")
        parent = cls._decode_parent(data, existing_cells, layers)
        style = cls._decode_style(data)
        value = get_optional_string_attribute(data, "value")

        geometry_data = data.find_all("mxGeometry")
        if len(geometry_data) > 1:
            raise XmlDecodingError("Found more than one geometry")
        elif len(geometry_data) == 0:
            raise XmlDecodingError("Found no geometry data")

        geometry_tag = geometry_data[0]
        if "vertex" not in data.attrs:
            raise XmlDecodingError("Cell is no Geometry")

        x = float(get_string_attribute(geometry_tag, "x", "0"))
        y = float(get_string_attribute(geometry_tag, "y", "0"))

        if isinstance(parent, GeometryCell):
            x += parent.top_left.x
            y += parent.top_left.y

        top_left = Point(x, y)
        bottom_right = Point(top_left.x + float(get_string_attribute(geometry_tag, "width")),
                             top_left.y + float(get_string_attribute(geometry_tag, "height")))

        out = GeometryCell(cell_id, style, value, parent, top_left, bottom_right)
        return out
