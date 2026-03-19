"""Module for the DrawIoExporter class and its Exceptions."""
import logging
import os
from pathlib import Path
from typing import Optional

from py_draw_io.document import Document

DEFAULT_DRAWIO_LOCATION = Path("/Applications/draw.io.app/Contents/MacOS/draw.io")
DEFAULT_QUALITY = 5
DEFAULT_TEMP_DIR = Path("temp")


class ElementNotFoundError(Exception):
    """Raised when trying to export an element that doesn't exist."""


class ExportFailedError(Exception):
    """Exception raised if the draw.io export command fails."""


class IllegalExtensionError(Exception):
    """Exception raised if anything but a .drawio or .xml is to be exported."""


class DrawIoExporter:
    """Handles the export of draw.io diagrams into png images."""

    _draw_io: Path
    _quality: int
    _temp: Path
    _logger: logging.Logger

    def __init__(self, draw_io: Path = DEFAULT_DRAWIO_LOCATION,
                 quality: int = DEFAULT_QUALITY,
                 temp_dir: Path = DEFAULT_TEMP_DIR):
        """
        Create a new instance for the DrawIoExporter class.

        :param draw_io: Path to the draw.io executable
        :param quality: Quality index for the draw.io export. Can remain the default if no problems arise
        :param temp_dir: Directory where temporary diagrams are stored that need to be created
        if only a part of a diagram is to be exported
        """
        self._draw_io = draw_io
        self._quality = quality
        self._temp = temp_dir
        self._logger = logging.getLogger(self.__class__.__name__)

    def _export(self, file: Path, page: str, out_path: Path) -> None:
        """Export the given diagram using the draw.io executable."""
        if out_path.is_file():
            os.remove(out_path)
        export_com = f"{self._draw_io} {file} --export -p {page} -s {self._quality} -t -o {out_path} --theme light"
        return_code = os.system(export_com)
        if not os.path.isfile(out_path):
            raise ExportFailedError(return_code)

    def _create_default_path(self, page: str, limit_export: Optional[str]) -> Path:
        """Create a default path for image exports based on the file name and exported area."""
        out_path = self._temp
        if limit_export:
            out_path /= f"{page}__{limit_export}.png"
        else:
            out_path /= f"{page}.png"
        return out_path

    def _get_temp_diagram_path(self, source: Path, page_name: str, limit_export: str) -> Path:
        """Create a path for a temporary diagram based on the file/page name and exported area."""
        source_file_name = Path(source).name.rstrip(".drawio").rstrip(".xml")
        target_file_name = f"{source_file_name}_{page_name}_{limit_export}.drawio"
        temp_file_path = self._temp / "diagrams" / target_file_name
        os.makedirs(temp_file_path.parent, exist_ok=True)
        return temp_file_path

    def _build_temp_file(self, source: Path, page_name: str, limit_export: str) -> Path:
        """Create a temporary diagram only containing the exported page with the specific elements wanted."""
        file_path = self._get_temp_diagram_path(source, page_name, limit_export)
        doc = Document.load(source)
        page = doc.get_diagram(page_name)
        doc.diagrams = [page]
        page.cells.remove_cells_outside_boundary(limit_export)
        doc.save(file_path)
        return file_path

    def _export_part_of_diagram(self, source: Path, page_name: str, out_path: Path, limit_export: str) -> None:
        """Export only a part of a diagram."""
        temp_file = self._build_temp_file(source, page_name, limit_export)
        self._export(temp_file, page_name, out_path)

    def export(self, source: Path, page: str, out_path: Optional[Path], limit_export: Optional[str]) -> None:
        """
        Export the given diagram (or a part of it) into an image.

        :param source: Location of the diagram to export
        :param page: Name of the sheet to export
        :param out_path: Full path to the output location
        :param limit_export: If set to an ID of any object on the page, only arrows/geometries
         enclosed by it will be exported
        :return: None
        """
        if not source.is_file():
            raise FileNotFoundError(f"{source} is not a file")
        if not source.name.endswith(".drawio"):
            raise IllegalExtensionError(f"{source} is neither a .drawio nor .xml file")
        if out_path is None:
            out_path = self._create_default_path(page, limit_export)
        os.makedirs(out_path.parent, exist_ok=True)

        if limit_export is None:
            self._export(source, page, out_path)
        else:
            self._export_part_of_diagram(source, page, out_path, limit_export)
