"""Module for the CacheFile class."""
from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import List, Dict

from pydantic import BaseModel

DEFAULT_CACHE_FILE = Path(".py_draw_io_cache")


class FileCache(BaseModel):
    hash: str
    files: List[str]

    @classmethod
    def new(cls, file_hash: str) -> FileCache:
        """
        Create a new FileCache object.

        :param file_hash: Hash of the source file
        :return:
        """
        return FileCache(hash=file_hash, files=[])


class CacheFile(BaseModel):
    """Class managing the module cache file."""
    created: datetime.datetime
    updated: datetime.datetime
    files: Dict[str, FileCache]

    @classmethod
    def load(cls, path: Path = DEFAULT_CACHE_FILE) -> CacheFile:
        """
        Load a cache file from disk.

        :param path: Path to the file to load
        :return: The loaded cache file
        """
        with open(path, "r") as file_p:
            data = json.load(file_p)
        return CacheFile.model_validate(data)

    def save(self, path: Path = DEFAULT_CACHE_FILE) -> None:
        """
        Save the cache file to disk.

        :param path: Path where the file gets saved
        :return: None
        """
        self.updated = datetime.datetime.now()
        with open(path, "w") as file_p:
            json.dump(self.model_dump(), file_p, indent=2)

    @classmethod
    def new(cls) -> CacheFile:
        """
        Create a new cache file.

        :return: The newly created CacheFile object
        """
        return CacheFile(created=datetime.datetime.now(), updated=datetime.datetime.now(), files={})
