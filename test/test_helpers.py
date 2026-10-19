import pytest
from bs4 import Tag
from bs4.element import AttributeValueList

from py_draw_io.errors import XmlDecodingError
from py_draw_io.helpers import get_optional_string_attribute, get_string_attribute


def test_get_string_attribute_success():
    attrs: dict[str, str | AttributeValueList] = {
        "test_list": AttributeValueList(["val1", "val2"]),
        "test_str": "t_val",
    }
    tag = Tag(name="mxCell", attrs=attrs)

    assert get_string_attribute(tag, "test_str") == "t_val"

    with pytest.raises(XmlDecodingError):
        _ = get_string_attribute(tag, "test_list")

    with pytest.raises(XmlDecodingError):
        _ = get_string_attribute(tag, "not_existent")

    assert get_string_attribute(tag, "not_existent", "default33") == "default33"


def test_get_optional_string_attribute():
    attrs: dict[str, str | AttributeValueList] = {
        "test_list": AttributeValueList(["val1", "val2"]),
        "test_str": "t_val",
    }
    tag = Tag(name="mxCell", attrs=attrs)

    assert get_optional_string_attribute(tag, "test_str") == "t_val"
    assert get_optional_string_attribute(tag, "not_existent") is None
