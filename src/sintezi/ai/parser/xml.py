from typing import Generic, TypeVar

from pydantic_xml import BaseXmlModel

from .base import ResponseParser
from .response_format import ResponseFormatCapability

TResult = TypeVar("TResult", bound=BaseXmlModel)


class XmlParser(ResponseParser[TResult], Generic[TResult]):
    def __init__(self, model_type: type[TResult]) -> None:
        self._model_type = model_type

    @property
    def returns(self) -> type[TResult]:
        return self._model_type

    def validate(self, content: str) -> TResult:
        return self._model_type.from_xml(content)

    def to_response_format(self, capabilities: set[ResponseFormatCapability]) -> dict | None:
        return None
