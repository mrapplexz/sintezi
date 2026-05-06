import openai

from sintezi.ai.parser import ResponseFormatCapability


class AiContext:
    def __init__(
        self,
        client: openai.AsyncClient,
        response_format_capabilities: set[ResponseFormatCapability],
    ) -> None:
        self._async_client = client
        self._response_format_capabilities = response_format_capabilities

    @property
    def async_client(self) -> openai.AsyncClient:
        return self._async_client

    @property
    def response_format_capabilities(self) -> set[ResponseFormatCapability]:
        return self._response_format_capabilities
