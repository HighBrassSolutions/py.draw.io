"""Module for the CacheFile class."""
from __future__ import annotations

import datetime
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from pydantic import BaseModel

DEFAULT_CACHE_FILE = Path(".py_draw_io_cache")


class CacheValidationError(Exception):
    """Raised if a file is not part of the cache during validation."""


class FileCache(BaseModel):
    """Cache for a single diagram file object."""

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
    @lru_cache
    def _get_file_hash(cls, source_file: Path) -> str:
        hasher = hashlib.sha256()
        with open(source_file, "rb") as file_p:
            while chunk := file_p.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def add_to_cache(self, source_diagram_file: Path, target_image_file: Path) -> None:
        """
        Register file in the cache.

        :param source_diagram_file: Diagram the image is to be exported from
        :param target_image_file: Image to be exported from the diagram
        :return: None
        """
        source_file_hash = self._get_file_hash(source_diagram_file)
        try:
            file_cache = self.files[source_diagram_file.as_posix()]
        except KeyError:
            file_cache = FileCache.new(source_file_hash)
            self.files[source_diagram_file.as_posix()] = file_cache

        if file_cache.hash != source_file_hash:
            file_cache = FileCache.new(source_file_hash)
            self.files[source_diagram_file.as_posix()] = file_cache

        target_image_path = target_image_file.as_posix()
        if target_image_path not in file_cache.files:
            file_cache.files.append(target_image_path)

    def check_file(self, source_diagram_file: Path, target_image_file: Path) -> None:
        """
        Check if the file is part of the cache.

        :param source_diagram_file: Diagram the image is to be exported from
        :param target_image_file: Image to be exported from the diagram
        :raises CacheValidationError: If the hash of source diagram does not match the one in cache
                                      or the target file is not part of the cache
        :return: None
        """
        source_file_hash = self._get_file_hash(source_diagram_file)
        try:
            file_cache = self.files[source_diagram_file.as_posix()]
        except KeyError:
            raise CacheValidationError("Source File was not found in cache")

        if file_cache.hash != source_file_hash:
            raise CacheValidationError("Source File hash does not match cached one")

        target_image_path = target_image_file.as_posix()
        if target_image_path not in file_cache.files:
            raise CacheValidationError("Target File was not found in cache")

    @classmethod
    def load(cls, path: Path = DEFAULT_CACHE_FILE, create_if_necessary: bool = False) -> CacheFile:
        """
        Load a cache file from disk.

        :param path: Path to the file to load
        :param create_if_necessary: Return an empty cache file object if no cache file exists
        :return: The loaded cache file
        """
        try:
            with open(path, "r") as file_p:
                data = json.load(file_p)
            return CacheFile.model_validate(data)
        except FileNotFoundError as err:
            if create_if_necessary:
                return CacheFile.new()
            raise err

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
