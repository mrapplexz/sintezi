# Quick start

This guide walks through using sintezi to generate structured synthetic data with an LLM.

## 1. Install sintezi

```bash
pip install sintezi
```

## 2. Define your data models

```python
from pydantic import BaseModel

class UserQuery(BaseModel):
    question: str
    context: str

class GeneratedAnswer(BaseModel):
    answer: str
    confidence: float
```

## 3. Create an AI context

```python
from openai import AsyncOpenAI
from sintezi.ai.context import ai_context_from_openai

client = AsyncOpenAI(api_key="your-api-key")
ctx = ai_context_from_openai(client)
```

## 4. Configure the structured call

```python
from sintezi.ai.executor import AiCallParameters, StructuredAiCallConfig, StructuredAiCall
from sintezi.ai.formatter import auto_formatter_for_type
from sintezi.ai.parser import auto_parser_for_type

config = StructuredAiCallConfig(
    system_message="You are a helpful assistant that answers questions based on context.",
    parameters=AiCallParameters(
        model="gpt-4o-mini",
        temperature=0.7,
    ),
)

ai_call = StructuredAiCall(
    ctx=ctx,
    config=config,
    formatter=auto_formatter_for_type(UserQuery),
    parser=auto_parser_for_type(GeneratedAnswer),
    retry_policy=None,
)
```

## 5. Execute

```python
query = UserQuery(
    question="What is the capital of France?",
    context="France is a country in Europe.",
)
result = await ai_call(query)
print(f"Answer: {result.answer} (confidence: {result.confidence})")
```

## What happens under the hood

1. **Formatting** — `UserQuery` is converted to the appropriate format (JSON by default)
2. **API call** — Sent to OpenAI with the configured parameters
3. **Retry logic** — Network errors and validation failures are retried separately
4. **Parsing** — Response is validated against `GeneratedAnswer` schema
5. **Result** — Typed Pydantic model is returned

## Next steps

- [Formatters](formatters.md) — customize input formatting
- [Parsers](parsers.md) — customize response parsing
- [Retry policies](retry.md) — configure retry behavior
