"""Module for the ArrowCell class."""
from __future__ import annotations
from typing import Union, List, Optional, Dict
from bs4 import Tag

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.cell_collection import CellCollection
from py_draw_io.errors import XmlDecodingError
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute
from py_draw_io.layer import Layer
from py_draw_io.point import Point
from py_draw_io.cell import Cell


class ArrowCell(Cell):
    """Represents a Cell containing an Arrow."""

    source: Union[Cell, Point]
    target: Union[Cell, Point]
    waypoints: List[Point]

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]],
                 value: Optional[str], parent: Optional[Cell],
                 source: Union[Cell, Point], target: Union[Cell, Point], waypoints: List[Point]):
        """
        Create a new instance of the ArrowCell class.

        :param cell_id: ID of the cell
        :param style: Styling information for the cell
        :param value: Content of the cells text field
        :param parent: Parent cell (if there is one)
        :param source: Source of the arrow. Can either be another Cell or a Point
        :param target: Target of the arrow. Can either be another Cell or a Point
        :param waypoints: Additional points the arrow goes through between source and target
        """
        super().__init__(cell_id, style, value, parent)
        self.source = source
        self.target = target
        self.waypoints = waypoints
        self.contains_geometry = True

    def __repr__(self) -> str:
        if self.waypoints:
            middle = f"-> {' -> '.join([str(x) for x in self.waypoints])} ->"
        else:
            middle = "->"
        return f"ArrowCell({self.id})[{self.source} {middle} {self.target}]"

    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
        return self.source.fits_inside(other) and self.target.fits_inside(other)

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        :return: The created XML tag
        """
        base = super().to_xml()
        base.attrs["edge"] = "1"

        out = Tag(name="mxGeometry")
        out.attrs["relative"] = "1"
        out.attrs["as"] = "geometry"

        if isinstance(self.source, Cell):
            base.attrs["source"] = self.source.id
        else:
            source = Tag(name="mxPoint")
            source.attrs["x"] = str(self.source.x)
            source.attrs["y"] = str(self.source.y)
            source.attrs["as"] = "sourcePoint"
            out.append(source)
        if isinstance(self.target, Cell):
            base.attrs["target"] = self.target.id
        else:
            target = Tag(name="mxPoint")
            target.attrs["x"] = str(self.target.x)
            target.attrs["y"] = str(self.target.y)
            target.attrs["as"] = "targetPoint"
            out.append(target)

        if self.waypoints:
            waypoint_tags = Tag(name="Array")
            waypoint_tags.attrs["as"] = "points"
            for waypoint in self.waypoints:
                waypoint_tag = Tag(name="mxPoint")
                waypoint_tag.attrs["x"] = str(waypoint.x)
                waypoint_tag.attrs["y"] = str(waypoint.y)
                waypoint_tags.append(waypoint_tag)
            out.append(waypoint_tags)

        base.append(out)
        return base

    @classmethod
    def from_xml(cls, data: Tag, existing_cells: CellCollection, layers: List[Layer]) -> ArrowCell:
        """
        Create a ArrowCell from the given xml data.

        :param data: XML tag to create the ArrowCell from
        :param existing_cells: Cells already parsed from the XML document
        :param layers: Layers parsed from the XML document
        :return: The created ArrowCell
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
        if "edge" not in data.attrs:
            raise XmlDecodingError("Geometry is no Arrow")

        source: Union[Cell, Point, None] = None
        if "source" in data.attrs:
            source = existing_cells.find_by_id(get_string_attribute(data, "source"))

        target: Union[Cell, Point, None] = None
        if "target" in data.attrs:
            target = existing_cells.find_by_id(get_string_attribute(data, "target"))

        points = geometry_tag.find_all("mxPoint")
        waypoints = []
        for point in points:
            point_obj = Point(float(get_string_attribute(point, "x")), float(get_string_attribute(point, "y")))
            point_type = point.get("as")
            if point_type is None:
                waypoints.append(point_obj)
            elif point_type == "sourcePoint":
                if source is not None:
                    raise XmlDecodingError("Arrow has more than one source defined")
                source = point_obj
            elif point_type == "targetPoint":
                if target is not None:
                    raise XmlDecodingError("Arrow has more than one target defined")
                target = point_obj
            else:
                raise XmlDecodingError(f"Illegal point type: {point_type}")

        if source is None:
            raise XmlDecodingError("Arrow has no source specified")

        if target is None:
            raise XmlDecodingError("Arrow has no target specified")

        out = ArrowCell(cell_id, style, value, parent, source, target, waypoints)
        return out
