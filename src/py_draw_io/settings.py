"""Module for the settings class."""


class Settings:
    """Class handling the module settings."""

    cache_results: bool

    def __init__(self, cache_results: bool = False) -> None:
        """
        Create a new instance of the Settings class.

        :param cache_results: Whether Exporters should cache results of exports and skip future exports if cached results are present.
        """
        self.cache_results = cache_results
