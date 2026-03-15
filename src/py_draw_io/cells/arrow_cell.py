from typing import Union, List, Optional, Dict
from bs4 import Tag

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.cell_collection import CellCollection
from py_draw_io.errors import XmlDecodingError
from py_draw_io.helpers import get_string_attribute, get_optional_string_attribute
from py_draw_io.point import Point
from py_draw_io.cells.cell import Cell


class ArrowCell(Cell):
    source: Union[Cell, Point]
    target: Union[Cell, Point]
    waypoints: List[Point]

    def __init__(self, cell_id: str, style: Optional[Dict[str, Union[int, str, None]]],
                 value: Optional[str], parent: Optional[Cell],
                 source: Union[Cell, Point], target: Union[Cell, Point], waypoints: List[Point]):
        super().__init__(cell_id, style, value, parent)
        self.source = source
        self.target = target
        self.waypoints = waypoints
        self.contains_geometry = True

    def __repr__(self):
        if self.waypoints:
            middle = f"-> {' -> '.join([str(x) for x in self.waypoints])} ->"
        else:
            middle = "->"
        return f"ArrowCell({self.id})[{self.source} {middle} {self.target}]"

    def __eq__(self, other):
        if not isinstance(other, ArrowCell):
            raise TypeError(f"Cannot compare ArrowCell with {type(other)}")
        if self.source != other.source:
            return False
        if self.target != other.target:
            return False
        if len(self.waypoints) != len(other.waypoints):
            return False
        for waypoint in self.waypoints:
            if waypoint not in other.waypoints:
                return False
        return True

    def fits_inside(self, other: BoundaryContainer) -> bool:
        return self.source.fits_inside(other) and self.target.fits_inside(other)

    def to_xml(self) -> Tag:
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
    def from_xml(cls, data: Tag, existing_cells: CellCollection) -> ArrowCell:
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
        if "edge" not in data.attrs:
            raise XmlDecodingError("Geometry is no Arrow")

        if "source" in data.attrs:
            source = existing_cells.find_by_id(get_string_attribute(data, "source"))
        else:
            source = None
        if "target" in data.attrs:
            target = existing_cells.find_by_id(get_string_attribute(data, "target"))
        else:
            target = None

        points = geometry_tag.find_all("mxPoint")
        waypoints = []
        for point in points:
            point_obj = Point(float(get_string_attribute(point, "x")), float(get_string_attribute(point, "y")))
            point_type = point.get("as")
            if point_type is None:
                waypoints.append(point_obj)
            elif point_type == "sourcePoint":
                if source is not None:
                    raise XmlDecodingError(f"Arrow has more than one source defined")
                source = point_obj
            elif point_type == "targetPoint":
                if target is not None:
                    raise XmlDecodingError(f"Arrow has more than one target defined")
                target = point_obj
            else:
                raise XmlDecodingError(f"Illegal point type: {point_type}")

        if source is None:
            raise XmlDecodingError(f"Arrow has no source specified")

        if target is None:
            raise XmlDecodingError(f"Arrow has no target specified")
        out = ArrowCell(cell_id, style, value, parent, source, target, waypoints)

        if parent is not None:
            parent.children.append(out)
        return out
