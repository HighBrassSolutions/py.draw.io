"""Helper functions for py_draw_io."""

from bs4 import Tag

from py_draw_io.errors import XmlDecodingError


def get_string_attribute(data: Tag, key: str, default: str | None = None) -> str:
    """
    Grabs the attribute from the passed tag and makes sure it is a string.

    :param data: XML tag to get the attribute from
    :param key: Name of the attribute to grab
    :param default: Default value to return if the attribute does not exist
    :return: The value of the attribute
    :raises XmlDecodingError: If the attribute does not exist or is not a string
    """
    if key not in data.attrs:
        if default is not None:
            return default
        raise XmlDecodingError(f"'{key}' attribute does not exist'")
    value = data.attrs[key]
    if not isinstance(value, str):
        raise XmlDecodingError(f"'{key}' attribute must be a string'")
    return value


def get_optional_string_attribute(data: Tag, key: str) -> str | None:
    """
    Grabs the attribute from the passed tag and makes sure it is either a string or does not exist.

    :param data: XML tag to get the attribute from
    :param key: Name of the attribute to grab
    :return: The value of the attribute if it exists, None otherwise
    :raises XmlDecodingError: If the attribute exists but is not a string
    """
    if key not in data.attrs:
        return None
    return get_string_attribute(data, key)
