from __future__ import annotations
from bs4 import Tag

from py_draw_io.helpers import get_string_attribute

DEFAULT_ATTRS = {"grid": 1, "guides": 10, "tooltips": 1,
                 "connect": 1, "arrows": 1, "fold": 1, "page": 1,
                 "pageScale": 1, "math": 0, "shadow": 0}


class GraphModel:
    grid_size: int
    page_width: int
    page_height: int

    def __init__(self, grid_size: int, page_width: int, page_height: int) -> None:
        self.grid_size = grid_size
        self.page_width = page_width
        self.page_height = page_height

    def __repr__(self) -> str:
        return f"GraphModel(grid_size={self.grid_size}, page_width={self.page_width}, page_height={self.page_height})"

    def to_xml(self) -> Tag:
        out = Tag(name="mxGraphModel")
        out.attrs["gridSize"] = str(self.grid_size)
        out.attrs["pageWidth"] = str(self.page_width)
        out.attrs["pageHeight"] = str(self.page_height)
        for attr, val in DEFAULT_ATTRS.items():
            out.attrs[attr] = str(val)
        return out

    @classmethod
    def from_xml(cls, data: Tag) -> GraphModel:
        return cls(int(get_string_attribute(data, "gridSize")),
                   int(get_string_attribute(data, "pageWidth")),
                   int(get_string_attribute(data, "pageHeight")))
