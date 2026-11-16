"""Module for the BoundaryContainer class."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_draw_io.point import Point


class BoundaryContainer:
    """Abstract class defining the interface for draw.io boundary checks."""

    top_left: Point
    bottom_right: Point
