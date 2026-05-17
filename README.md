# sintezi

Synthetic data generation that actually doesn't hurt.

[![PyPI](https://img.shields.io/pypi/v/sintezi?color=blue)](https://pypi.org/project/sintezi/)
[![Python](https://img.shields.io/pypi/pyversions/sintezi)](https://pypi.org/project/sintezi/)
[![License](https://img.shields.io/github/license/mrapplexz/sintezi)](LICENSE)
[![CI](https://github.com/mrapplexz/sintezi/actions/workflows/release.yml/badge.svg)](https://github.com/mrapplexz/sintezi/actions/workflows/release.yml)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://mrapplexz.github.io/sintezi/)

A type-safe Python library for generating synthetic data using LLMs. Built with structured outputs, automatic retry policies, and support for multiple response formats (JSON, XML).

## Features

- **Type-safe** — Pydantic models for requests and responses with full type hints
- **Multiple formats** — JSON, XML, plain text, or custom formatters
- **Smart retry** — Separate retry policies for network errors and validation failures
- **Auto-parsing** — Automatic format selection based on Pydantic models
- **LLM-agnostic** — Works with any OpenAI-compatible API

## Installation

```bash
pip install sintezi
```

**Requirements:** Python 3.11+

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

## Core concepts

| Concept | Description |
|---------|-------------|
| **AiContext** | Holds the OpenAI client and retry configuration |
| **Formatter** | Converts Pydantic models to LLM-readable format (JSON/XML/text) |
| **Parser** | Validates and parses LLM responses back to Pydantic models |
| **RetryPolicy** | Separate retry logic for network errors and validation failures |
| **StructuredAiCall** | Main executor that orchestrates formatting, API calls, and parsing |

## Custom retry policies

```python
from sintezi.ai.context import RetryPolicy, RetryParameters

retry_policy = RetryPolicy(
    validation=RetryParameters(
        stop_after_attempt=5,
        wait_initial=1.0,
        wait_max=10.0,
    ),
    network=RetryParameters(
        stop_after_attempt=3,
        wait_initial=2.0,
        wait_max=30.0,
    ),
)

ctx = ai_context_from_openai(client, retry_policy=retry_policy)
```

## Response formats

sintezi automatically selects the best format based on your Pydantic model:

- **JSON** — default for most models, uses OpenAI's `response_format`
- **XML** — for complex nested structures (requires `pydantic-xml`)
- **Plain text** — for simple string responses

Override with explicit formatters:

```python
from sintezi.ai.formatter import JsonFormatter, XmlFormatter

formatter = JsonFormatter(model=UserQuery)
parser = XmlFormatter(model=GeneratedAnswer)
```

## Load configuration from files

Store prompts and parameters separately:

```python
from pathlib import Path

# Expects:
# - config.txt (system message)
# - config.json (AiCallParameters as JSON)

ai_call = StructuredAiCall.from_files(
    ctx=ctx,
    path=Path("config"),  # will load config.txt and config.json
    formatter=auto_formatter_for_type(UserQuery),
    parser=auto_parser_for_type(GeneratedAnswer),
)
```

## Documentation

Full documentation is available at [https://mrapplexz.github.io/sintezi/](https://mrapplexz.github.io/sintezi/)

## Development

```bash
# Install dependencies
uv sync --group dev

# Run linting
make lint

# Run tests
make test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full development guide (coming soon).

## License

[MIT](LICENSE)
