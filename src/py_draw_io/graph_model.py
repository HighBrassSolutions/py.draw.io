"""Module containing the GraphModel class."""
from __future__ import annotations

from bs4 import Tag

from py_draw_io.helpers import get_string_attribute

DEFAULT_ATTRS = {"grid": 1, "guides": 10, "tooltips": 1,
                 "connect": 1, "arrows": 1, "fold": 1, "page": 1,
                 "pageScale": 1, "math": 0, "shadow": 0}


class GraphModel:
    """Represents a graph model."""

    grid_size: int
    page_width: int
    page_height: int

    def __init__(self, grid_size: int, page_width: int, page_height: int) -> None:
        """
        Create a new Instance of the GraphModel class.

        Args:
            grid_size: The grid size of the diagram
            page_width: The width of the diagram page
            page_height: The width of the diagram page
        """
        self.grid_size = grid_size
        self.page_width = page_width
        self.page_height = page_height

    def __repr__(self) -> str:
        return f"GraphModel(grid_size={self.grid_size}, page_width={self.page_width}, page_height={self.page_height})"

    def to_xml(self) -> Tag:
        """
        Convert the GraphModel to a XML tag.

        Returns:
            The created XML tag
        """
        out = Tag(name="mxGraphModel")
        out.attrs["gridSize"] = str(self.grid_size)
        out.attrs["pageWidth"] = str(self.page_width)
        out.attrs["pageHeight"] = str(self.page_height)
        for attr, val in DEFAULT_ATTRS.items():
            out.attrs[attr] = str(val)
        return out

    @classmethod
    def from_xml(cls, data: Tag) -> GraphModel:
        """
        Create a GraphModel from the given xml data.

        Args:
            data: XML tag to create the GraphModel from

        Returns:
            The created GraphModel

        Raises:
            XmlDecodingError: If any of the required attributes is missing
        """
        return cls(int(get_string_attribute(data, "gridSize")),
                   int(get_string_attribute(data, "pageWidth")),
                   int(get_string_attribute(data, "pageHeight")))
