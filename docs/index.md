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
| **Formatter** | Converts structured objects to LLM-readable format (JSON/XML/text) |
| **Parser** | Validates and parses LLM responses back to structured objects |
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


class ProductInfo(BaseModel):
    name: str
    category: str
    key_features: list[str]


class ProductDescription(BaseModel):
    short_description: str
    detailed_description: str
    selling_points: list[str]


async def main():
    # Create OpenAI client
    client = AsyncOpenAI(api_key="your-api-key")
    ctx = ai_context_from_openai(client)

    # Configure the AI call
    config = StructuredAiCallConfig(
        system_message="You are a marketing copywriter that creates engaging product descriptions.",
        parameters=AiCallParameters(
            model="gpt-4o-mini",
            temperature=0.8,
        ),
    )

    # Create structured call with auto-detected formats
    ai_call = StructuredAiCall(
        ctx=ctx,
        config=config,
        formatter=auto_formatter_for_type(ProductInfo),
        parser=auto_parser_for_type(ProductDescription),
        retry_policy=None,  # Use default retry policy
    )

    # Execute
    product = ProductInfo(
        name="Wireless Noise-Cancelling Headphones",
        category="Electronics",
        key_features=["Active noise cancellation", "30-hour battery", "Bluetooth 5.0"],
    )
    result = await ai_call(product)
    print(f"Short: {result.short_description}")
    print(f"Detailed: {result.detailed_description}")
    print(f"Selling points: {result.selling_points}")


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
- [Executors](guide/executors.md) — available AI call executors
- [Formatters](guide/formatters.md) — JSON, XML, and custom formats
- [Parsers](guide/parsers.md) — response parsing and validation
- [Retry policies](guide/retry.md) — configuring retry behavior
- [API Reference](reference/index.md) — complete API documentation
