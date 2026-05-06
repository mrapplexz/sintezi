import abc
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest")


class RequestFormatter(abc.ABC, Generic[TRequest]):
    @abc.abstractmethod
    def format(self, content: TRequest) -> str: ...
