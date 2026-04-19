"""Module for the settings class."""
from pathlib import Path

from py_draw_io.cache import CacheFile

DEFAULT_CACHE_FILE = Path(".py_draw_io_cache")


class Settings:
    """Class handling the module settings."""

    use_cache: bool
    cache_file_location: Path
    cache_file: CacheFile

    def __init__(self, cache_results: bool = False, cache_file_location: Path = DEFAULT_CACHE_FILE) -> None:
        """
        Create a new instance of the Settings class.

        :param cache_results: Whether Exporters should cache results of exports
                              and skip future exports if cached results are present.
        :param cache_file_location: The location of the cache file.
        """
        self.use_cache = cache_results
        self.cache_file_location = cache_file_location
        self.cache_file = CacheFile.load(self.cache_file_location, create_if_necessary=True)

    def switch_cache_file(self, path: Path) -> None:
        """
        Switch the location of the global cache file.

        :param path: Path to the new cache file
        :return: None
        """
        self.cache_file_location = path
        self.cache_file = CacheFile.load(self.cache_file_location, create_if_necessary=True)
