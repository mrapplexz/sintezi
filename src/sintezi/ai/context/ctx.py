import openai

from sintezi.ai.parser import ResponseFormatCapability

from .retry import RetryParameters, RetryPolicy

_DEFAULT_RETRY_POLICY = RetryPolicy(
    network=RetryParameters(
        stop_after_attempt=5,
        stop_after_delay=None,
        wait_initial=0.25,
        wait_max=10,
    ),
    validation=RetryParameters(
        stop_after_attempt=5,
        stop_after_delay=None,
        wait_max=1,
        wait_initial=0,
    ),
)


class AiContext:
    def __init__(
        self,
        client: openai.AsyncClient,
        response_format_capabilities: set[ResponseFormatCapability],
        retry_policy: RetryPolicy | None,
    ) -> None:
        self._async_client = client
        self._response_format_capabilities = response_format_capabilities
        self._retry_policy = _DEFAULT_RETRY_POLICY.merge(retry_policy)

    @property
    def async_client(self) -> openai.AsyncClient:
        return self._async_client

    @property
    def response_format_capabilities(self) -> set[ResponseFormatCapability]:
        return self._response_format_capabilities

    @property
    def retry_policy(self) -> RetryPolicy:
        return self._retry_policy
