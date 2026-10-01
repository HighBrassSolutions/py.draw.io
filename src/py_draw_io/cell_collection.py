"""Module for the CellCollection class."""
from collections.abc import Iterator

from py_draw_io.boundary_container import BoundaryContainer
from py_draw_io.cell import Cell


class CellNotFoundError(Exception):
    """Raised if no cell was found in the search."""


class IllegalBoundaryError(Exception):
    """Raised if an illegal boundary is being used to remove cells outside boundaries."""


class CellCollection:
    """Manages a list of cells and provides functions to manage it and all children of its elements recursively."""

    _data: list[Cell]

    def __init__(self, data: list[Cell] | None = None) -> None:
        """
        Create a new instance of the CellCollection class.

        :param data: Can be a list of cells to initialize the collection with some cells
        """
        if data is None:
            self._data = []
        else:
            self._data = data

    def __repr__(self) -> str:
        return f"CellCollection[{len(self)} Elems]"

    def __len__(self) -> int:
        def _get_length(cell: Cell) -> int:
            return 1 + sum([_get_length(x) for x in cell.children])

        return sum([_get_length(x) for x in self._data])

    def __iter__(self) -> Iterator[Cell]:
        return iter(self._data)

    def __getitem__(self, index: int) -> Cell:
        return self._data[index]

    def append(self, cell: Cell) -> None:
        """
        Append a cell to the cell collection.

        :param cell: Cell to append
        :return: None
        """
        self._data.append(cell)

    def find_by_id(self, cell_id: str) -> Cell:
        """
        Search the collection for cells with the given cell id recursively.

        :param cell_id: ID to find a matching cell for
        :raises CellNotFoundError: If no cell was found for the given ID
        :return: The cell if one was found
        """

        def helper(data: list[Cell]) -> Cell | None:
            """Check the data for the wanted cell, try recursively with the children."""
            for cell in data:
                if cell.id == cell_id:
                    return cell
                if cell.children:
                    found = helper(cell.children)
                    if found:
                        return found
            return None

        found_cell = helper(self._data)
        if not found_cell:
            raise CellNotFoundError(cell_id)
        return found_cell

    def remove_cells_outside_boundary(self, boundary: BoundaryContainer | str) -> None:
        """
        Remove all cells outside the boundary from the cell collection.

        If a string is passed, a cell with a matching ID will be used.
        For cells with geometries, only the first parent gets checked, meaning if the parent does not fit the boundary,
        it gets removed together with all children.

        :param boundary: Either a BoundaryContainer or a String matching the ID of one of the Cells
        :raises CellNotFoundError: If a String was given but no matching cell was found
        :raises IllegalBoundaryError: If the found cell does not contain a geometry
        :return: None
        """
        boundary_container: BoundaryContainer
        if isinstance(boundary, str):
            found = self.find_by_id(boundary)
            if not isinstance(found, BoundaryContainer):
                raise IllegalBoundaryError(f"Detected Cell for id '{boundary}' has no geometry")
            boundary_container = found
        else:
            boundary_container = boundary

        def clean(cells: list[Cell]) -> list[Cell]:
            out = [x for x in cells if not x.contains_geometry or x.fits_inside(boundary_container)]
            for cell in out:
                cell.children = clean(cell.children)
            return out

        self._data = clean(self._data)
