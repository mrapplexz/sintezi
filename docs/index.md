# sintezi

Synthetic data generation that actually doesn't hurt.

A type-safe Python library for generating synthetic data using LLMs. Built with structured outputs, automatic retry policies, and support for multiple response formats (JSON, XML).

## Installation

```bash
pip install sintezi
```

**Requirements:** Python 3.11+

## Key concepts

| Concept | Description |
|---------|-------------|
| **AiContext** | Holds the OpenAI client and retry configuration |
| **Formatter** | Converts Pydantic models to LLM-readable format (JSON/XML/text) |
| **Parser** | Validates and parses LLM responses back to Pydantic models |
| **RetryPolicy** | Separate retry logic for network errors and validation failures |
| **StructuredAiCall** | Main executor that orchestrates formatting, API calls, and parsing |

## Quick start

```python
import asyncio
from pydantic import BaseModel
from openai import AsyncOpenAI
from sintezi.ai.context import ai_context_from_openai
from sintezi.ai.executor import AiCallParameters, StructuredAiCallConfig
from sintezi.ai.formatter import auto_formatter_for_type
from sintezi.ai.parser import auto_parser_for_type
from sintezi.ai.executor import StructuredAiCall


class UserQuery(BaseModel):
    question: str
    context: str


class GeneratedAnswer(BaseModel):
    answer: str
    confidence: float


async def main():
    # Create OpenAI client
    client = AsyncOpenAI(api_key="your-api-key")
    ctx = ai_context_from_openai(client)

    # Configure the AI call
    config = StructuredAiCallConfig(
        system_message="You are a helpful assistant that answers questions based on context.",
        parameters=AiCallParameters(
            model="gpt-4o-mini",
            temperature=0.7,
        ),
    )

    # Create structured call with auto-detected formats
    ai_call = StructuredAiCall(
        ctx=ctx,
        config=config,
        formatter=auto_formatter_for_type(UserQuery),
        parser=auto_parser_for_type(GeneratedAnswer),
        retry_policy=None,  # Use default retry policy
    )

    # Execute
    query = UserQuery(
        question="What is the capital of France?",
        context="France is a country in Europe.",
    )
    result = await ai_call(query)
    print(f"Answer: {result.answer} (confidence: {result.confidence})")


asyncio.run(main())
```

## Features

- **Type-safe** — Pydantic models for requests and responses with full type hints
- **Multiple formats** — JSON, XML, plain text, or custom formatters
- **Smart retry** — Separate retry policies for network errors and validation failures
- **Auto-parsing** — Automatic format selection based on Pydantic models
- **LLM-agnostic** — Works with any OpenAI-compatible API

## Next steps

- [Quick start guide](guide/quickstart.md) — detailed walkthrough
- [Formatters](guide/formatters.md) — JSON, XML, and custom formats
- [Parsers](guide/parsers.md) — response parsing and validation
- [Retry policies](guide/retry.md) — configuring retry behavior
- [API Reference](reference/index.md) — complete API documentation
