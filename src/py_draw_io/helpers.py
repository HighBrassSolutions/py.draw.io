from typing import Optional
from bs4 import Tag

from py_draw_io.errors import XmlDecodingError


def get_string_attribute(data: Tag, key: str, default: Optional[str] = None) -> str:
    """Grabs the attribute from the passed tag and makes sure it is a string"""
    if key not in data.attrs and default is not None:
        return default
    value = data.attrs[key]
    if not isinstance(value, str):
        raise XmlDecodingError(f"'{key}' attribute must be a string'")
    return value


def get_optional_string_attribute(data: Tag, key: str) -> Optional[str]:
    if key not in data.attrs:
        return None
    return get_string_attribute(data, key)
