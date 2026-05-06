from typing import TypeVar

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

from .base import ResponseParser
from .json import JsonParser, JsonResponseFormat
from .str import StrParser
from .xml import XmlParser

TResponse = TypeVar("TResponse")


def auto_parser_for_type(model_type: type[TResponse]) -> ResponseParser:
    if issubclass(model_type, BaseXmlModel):
        return XmlParser(model_type=model_type)
    elif issubclass(model_type, BaseModel):
        return JsonParser(model_type=model_type, response_format=JsonResponseFormat.json_schema)
    elif issubclass(model_type, str):
        return StrParser()
    else:
        raise ValueError(f"Unsupported model type {model_type}")
