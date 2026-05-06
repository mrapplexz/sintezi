from typing import Generic, TypeVar

from pydantic import BaseModel

from .base import RequestFormatter

TRequest = TypeVar("TRequest", bound=BaseModel)


class JsonFormatter(RequestFormatter[TRequest], Generic[TRequest]):
    def __init__(self, indent: int | None = None) -> None:
        self._indent = indent

    def format(self, content: TRequest) -> str:
        return content.model_dump_json(indent=self._indent or 0)
