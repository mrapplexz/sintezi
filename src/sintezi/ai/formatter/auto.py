from typing import TypeVar

from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

from .base import RequestFormatter
from .json import JsonFormatter
from .str import StrFormatter
from .xml import XmlFormatter

TRequest = TypeVar("TRequest")


def auto_formatter_for_type(model_type: type[TRequest], indent: int | None = None) -> RequestFormatter:
    if issubclass(model_type, BaseXmlModel):
        return XmlFormatter()
    elif issubclass(model_type, BaseModel):
        return JsonFormatter(indent=indent)
    elif issubclass(model_type, str):
        return StrFormatter()
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
