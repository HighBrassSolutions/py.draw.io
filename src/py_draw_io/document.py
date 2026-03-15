import os
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup, Tag

from .diagram import Diagram
from .errors import XmlDecodingError


class DiagramNotFoundError(Exception):
    """Raised if no diagram with the given name or id was found"""


class Document:
    diagrams: List[Diagram]
    host: str
    agent: str

    def __init__(self, diagrams: List[Diagram], host: str, agent: str):
        self.diagrams = diagrams
        self.host = host
        self.agent = agent

    def __len__(self) -> int:
        return len(self.diagrams)

    def get_diagram(self, identifier: str) -> Diagram:
        """
        Gets a specific diagram from the file

        :param identifier: Name or ID of the diagram to get
        :raises DiagramNotFoundError: If no diagram with the given name or id was found
        :return: The diagram if found
        """
        for diagram in self.diagrams:
            if diagram.id == identifier or diagram.name == identifier:
                return diagram
        raise DiagramNotFoundError(f"No diagram with name or id '{identifier}' was found")

    @classmethod
    def from_xml(cls, data: Tag) -> Document:
        diagrams = []
        for diagram_data in data.find_all("diagram"):
            diagrams.append(Diagram.from_xml(diagram_data))
        return cls(diagrams, data.attrs["host"], data.attrs["agent"])

    @classmethod
    def load(cls, path: Path) -> Document:
        """
        Loads the draw.io document from the specified path

        :param path: Path to load the document from
        :return: The document as an object
        """
        with open(path, 'r') as file_p:
            xml_data = BeautifulSoup(file_p.read(), "xml")
        if len(xml_data.contents) != 1:
            raise XmlDecodingError("Length of contents is not 1")
        data = xml_data.contents[0]
        if not isinstance(data, Tag):
            raise XmlDecodingError("Data is not a Tag")
        return cls.from_xml(data)

    def to_xml(self) -> Tag:
        out = Tag(name="mxfile")
        out.attrs["host"] = self.host
        out.attrs["agent"] = self.agent
        out.attrs["pages"] = str(len(self.diagrams))
        for diagram in self.diagrams:
            out.append(diagram.to_xml())
        return out

    def save(self, path: Path) -> None:
        """
        Saves the document to the specified path

        :param path: Path to save the document to
        :return: None
        """
        os.makedirs(path.parent, exist_ok=True)
        encoded = self.to_xml()
        soup = BeautifulSoup("", "xml")
        soup.append(encoded)
        with open(path, 'w') as file_p:
            file_p.write(soup.prettify())
