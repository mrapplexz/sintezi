# sintezi

Synthetic data generation that actually doesn't hurt.

[![PyPI](https://img.shields.io/pypi/v/sintezi?color=blue)](https://pypi.org/project/sintezi/)
[![Python](https://img.shields.io/pypi/pyversions/sintezi)](https://pypi.org/project/sintezi/)
[![License](https://img.shields.io/github/license/mrapplexz/sintezi)](LICENSE)
[![CI](https://github.com/mrapplexz/sintezi/actions/workflows/release.yml/badge.svg)](https://github.com/mrapplexz/sintezi/actions/workflows/release.yml)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://mrapplexz.github.io/sintezi/)

A type-safe Python library for generating synthetic data using LLMs. Built with structured outputs, automatic retry policies, and support for multiple response formats (JSON, XML).

**Why sintezi?** Unlike general-purpose LLM frameworks (LangChain, LlamaIndex), sintezi is focused on bulk synthetic data generation with explicit developer control:

- **Bulk generation first** — optimized for creating large synthetic datasets, not building chatbots or agents
- **Explicit control** — you define formats, parsers, and retry logic; no hidden prompt engineering or magic
- **Simple by design** — no memory systems, RAG pipelines, or high-level abstractions; just clean, predictable data generation

If you need agentic workflows, memory, or RAG, use LangChain. If you need to generate 10,000 structured examples with full control, use sintezi.

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
from pydantic import BaseModel
from openai import AsyncOpenAI
from sintezi.ai.context import ai_context_from_openai
from sintezi.ai.executor import StructuredAiCall, StructuredAiCallConfig, AiCallParameters
from sintezi.ai.formatter import auto_formatter_for_type
from sintezi.ai.parser import auto_parser_for_type

class ProductInfo(BaseModel):
    name: str
    category: str

class ProductDescription(BaseModel):
    description: str

# Setup
client = AsyncOpenAI(api_key="your-api-key")
ctx = ai_context_from_openai(client)

config = StructuredAiCallConfig(
    system_message="Generate product descriptions.",
    parameters=AiCallParameters(model="gpt-4o-mini"),
)

ai_call = StructuredAiCall(
    ctx=ctx,
    config=config,
    formatter=auto_formatter_for_type(ProductInfo),
    parser=auto_parser_for_type(ProductDescription),
)

# Generate
product = ProductInfo(name="Laptop", category="Electronics")
result = await ai_call(product)
print(result.description)
```

See the [quick start guide](https://mrapplexz.github.io/sintezi/guide/quickstart/) for a complete walkthrough.

## Documentation

Full documentation: [https://mrapplexz.github.io/sintezi/](https://mrapplexz.github.io/sintezi/)

- [Quick start guide](https://mrapplexz.github.io/sintezi/guide/quickstart/) — complete walkthrough with examples
- [Executors](https://mrapplexz.github.io/sintezi/guide/executors/) — available AI call executors
- [Formatters](https://mrapplexz.github.io/sintezi/guide/formatters/) — JSON, XML, custom formats
- [Parsers](https://mrapplexz.github.io/sintezi/guide/parsers/) — response parsing and validation
- [Retry policies](https://mrapplexz.github.io/sintezi/guide/retry/) — network and validation retry configuration
- [API Reference](https://mrapplexz.github.io/sintezi/reference/) — complete API documentation

## License

[MIT](LICENSE)
