import openai

from sintezi.ai.parser import ResponseFormatCapability

from .ctx import AiContext


def ai_context_from_openai(client: openai.AsyncClient) -> AiContext:
    return AiContext(
        client=client,
        response_format_capabilities={ResponseFormatCapability.json, ResponseFormatCapability.json_schema},
    )
