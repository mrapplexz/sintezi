from typing import Generic, TypeVar, cast

from pydantic_xml import BaseXmlModel

from .base import RequestFormatter

TRequest = TypeVar("TRequest", bound=BaseXmlModel)


class XmlFormatter(RequestFormatter[TRequest], Generic[TRequest]):
    def format(self, content: TRequest) -> str:
        return cast(str, content.to_xml(encoding="unicode"))
