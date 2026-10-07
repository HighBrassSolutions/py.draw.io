"""Module for the Document class and its exceptions."""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup, Tag

from .diagram import Diagram
from .helpers import get_string_attribute


class DiagramNotFoundError(Exception):
    """Raised if no diagram with the given name or id was found."""


class NoDrawioDocumentError(Exception):
    """Raised if no diagram data was found inside the file."""


class Document:
    """Class representing a draw.io document."""

    diagrams: list[Diagram]
    host: str
    agent: str

    def __init__(self, diagrams: list[Diagram], host: str, agent: str) -> None:
        """
        Create a new instance for the Document class.

        Args:
            diagrams: Diagrams (Pages) contained in this document
            host: Host as defined in the document header
            agent: Agent as defined in the document header
        """
        self.diagrams = diagrams
        self.host = host
        self.agent = agent

    def __len__(self) -> int:
        return len(self.diagrams)

    def get_diagram(self, identifier: str) -> Diagram:
        """
        Get a specific diagram from the file.

        Args:
            identifier: Name or ID of the diagram to get

        Returns:
            The diagram (if found)

        Raises:
            DiagramNotFoundError: If no diagram with the given name or id was found
        """
        for diagram in self.diagrams:
            if diagram.id == identifier or diagram.name == identifier:
                return diagram
        raise DiagramNotFoundError(f"No diagram with name or id '{identifier}' was found")

    @classmethod
    def from_xml(cls, data: Tag) -> Document:
        """
        Create a Document from the given xml data.

        Args:
            data: XML tag to create the GraphModel from

        Returns:
            The created Document

        Raises:
            XmlDecodingError: If parsing fails for any reason
        """
        diagrams = [Diagram.from_xml(diagram_data) for diagram_data in data.find_all("diagram")]
        return cls(diagrams, get_string_attribute(data, "host"), get_string_attribute(data, "agent"))

    @classmethod
    def load(cls, path: Path) -> Document:
        """
        Load the draw.io document from the specified path.

        Args:
            path: Path to load the document from

        Returns:
            The document as an object
        """
        with path.open() as file_p:
            xml_data = BeautifulSoup(file_p.read(), "xml")

        try:
            data = xml_data.find_all("mxfile")[0]
        except IndexError as err:
            raise NoDrawioDocumentError("No draw.io diagram tag (mxfile) was found inside the file") from err

        return cls.from_xml(data)

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        Returns:
            The created XML tag
        """
        out = Tag(name="mxfile")
        out.attrs["host"] = self.host
        out.attrs["agent"] = self.agent
        out.attrs["pages"] = str(len(self.diagrams))
        for diagram in self.diagrams:
            out.append(diagram.to_xml())
        return out

    def save(self, path: Path) -> None:
        """
        Save the document to the specified path.

        Args:
            path: Path to save the document to
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = self.to_xml()
        soup = BeautifulSoup("", "xml")
        soup.append(encoded)
        with path.open("w") as file_p:
            file_p.write(soup.prettify())
