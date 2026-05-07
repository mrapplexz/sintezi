from .base import ResponseFormatCapability, ResponseParser


class StrParser(ResponseParser[str]):
    @property
    def returns(self) -> type[str]:
        return str

    def validate(self, content: str) -> str:
        return content

    def to_response_format(self, capabilities: set[ResponseFormatCapability]) -> dict | None:
        return None
