"""Module for the Document class and its exceptions."""
from __future__ import annotations
import os
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup, Tag

from .diagram import Diagram
from .helpers import get_string_attribute


class DiagramNotFoundError(Exception):
    """Raised if no diagram with the given name or id was found."""


class NoDrawioDocumentError(Exception):
    """Raised if no diagram data was found inside the file."""


class Document:
    """Class representing a draw.io document."""

    diagrams: List[Diagram]
    host: str
    agent: str

    def __init__(self, diagrams: List[Diagram], host: str, agent: str):
        """
        Create a new instance for the Document class.

        :param diagrams: Diagrams (Pages) contained in this document
        :param host: Host as defined in the document header
        :param agent: Agent as defined in the document header
        """
        self.diagrams = diagrams
        self.host = host
        self.agent = agent

    def __len__(self) -> int:
        return len(self.diagrams)

    def get_diagram(self, identifier: str) -> Diagram:
        """
        Get a specific diagram from the file.

        :param identifier: Name or ID of the diagram to get
        :raises DiagramNotFoundError: If no diagram with the given name or id was found
        :return: The diagram (if found)
        """
        for diagram in self.diagrams:
            if diagram.id == identifier or diagram.name == identifier:
                return diagram
        raise DiagramNotFoundError(f"No diagram with name or id '{identifier}' was found")

    @classmethod
    def from_xml(cls, data: Tag) -> Document:
        """
        Create a Document from the given xml data.

        :param data: XML tag to create the GraphModel from
        :return: The created Document
        :raises XmlDecodingError: If parsing fails for any reason
        """
        diagrams = []
        for diagram_data in data.find_all("diagram"):
            diagrams.append(Diagram.from_xml(diagram_data))
        return cls(diagrams, get_string_attribute(data, "host"), get_string_attribute(data, "agent"))

    @classmethod
    def load(cls, path: Path) -> Document:
        """
        Load the draw.io document from the specified path.

        :param path: Path to load the document from
        :return: The document as an object
        """
        with open(path, 'r') as file_p:
            xml_data = BeautifulSoup(file_p.read(), "xml")

        try:
            data = xml_data.find_all("mxfile")[0]
        except IndexError:
            raise NoDrawioDocumentError("No draw.io diagram tag (mxfile) was found inside the file")

        return cls.from_xml(data)

    def to_xml(self) -> Tag:
        """
        Create an XML structure representing this class.

        :return: The created XML tag
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

        :param path: Path to save the document to
        :return: None
        """
        os.makedirs(path.parent, exist_ok=True)
        encoded = self.to_xml()
        soup = BeautifulSoup("", "xml")
        soup.append(encoded)
        with open(path, 'w') as file_p:
            file_p.write(soup.prettify())
