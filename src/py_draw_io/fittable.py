from abc import ABC, abstractmethod

from py_draw_io.boundary_container import BoundaryContainer


class Fittable(ABC):
    @abstractmethod
    def fits_inside(self, other: BoundaryContainer) -> bool:
        """Determines, if this object is fully contained within the other one."""
