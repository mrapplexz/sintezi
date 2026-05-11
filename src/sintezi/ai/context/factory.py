import openai

from sintezi.ai.parser import ResponseFormatCapability

from .ctx import AiContext
from .retry import RetryPolicy


def ai_context_from_openai(client: openai.AsyncClient, retry_policy: RetryPolicy | None = None) -> AiContext:
    return AiContext(
        client=client,
        response_format_capabilities={ResponseFormatCapability.json, ResponseFormatCapability.json_schema},
        retry_policy=retry_policy,
    )
