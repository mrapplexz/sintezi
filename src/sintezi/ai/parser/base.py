import abc
from typing import Generic, TypeVar

from .response_format import ResponseFormatCapability

TResult = TypeVar("TResult")


class ResponseParser(abc.ABC, Generic[TResult]):
    @property
    @abc.abstractmethod
    def returns(self) -> type[TResult]: ...

    @abc.abstractmethod
    def validate(self, content: str) -> TResult: ...

    @abc.abstractmethod
    def to_response_format(self, capabilities: set[ResponseFormatCapability]) -> dict | None: ...
