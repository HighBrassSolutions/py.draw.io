from bs4 import Tag

from py_draw_io.errors import XmlDecodingError

DEFAULT_ATTRS = {"grid": 1, "guides": 10, "tooltips": 1,
                 "connect": 1, "arrows": 1, "fold": 1, "page": 1,
                 "pageScale": 1, "math": 0, "shadow": 0}


class GraphModel:
    gridSize: int
    pageWidth: int
    pageHeight: int

    def __init__(self, grid_size: int, page_width: int, page_height: int) -> None:
        self.grid_size = grid_size
        self.page_width = page_width
        self.page_height = page_height

    def __repr__(self):
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
        grid_size = data.attrs["gridSize"]
        if not isinstance(grid_size, str):
            raise XmlDecodingError("'gridSize' attribute must be a string'")

        page_width = data.attrs["pageWidth"]
        if not isinstance(page_width, str):
            raise XmlDecodingError("'pageWidth' attribute must be a string'")

        page_height = data.attrs["pageHeight"]
        if not isinstance(page_height, str):
            raise XmlDecodingError("'pageHeight' attribute must be a string'")

        return cls(int(grid_size),
                   int(page_width),
                   int(page_height))
