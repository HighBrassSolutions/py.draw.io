"""Module for the 'Fittable' interface."""
from abc import ABC, abstractmethod

from py_draw_io.boundary_container import BoundaryContainer


class Fittable(ABC):
    """Interface for all objects that might need to fit into a boundary."""

    @abstractmethod
    def fits_inside(self, other: BoundaryContainer) -> bool:
        """
        Determine if this object is fully contained within the other one.

        :param other: Container defining the boundary this object needs to be fully enclosed by
        :return:
        """
