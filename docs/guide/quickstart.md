# Quick start

This guide walks through using sintezi to generate structured synthetic data with an LLM.

## 1. Install sintezi

```bash
pip install sintezi
```

## 2. Define your data models

```python
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    category: str
    key_features: list[str]

class ProductDescription(BaseModel):
    short_description: str
    detailed_description: str
    selling_points: list[str]
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
    system_message="You are a marketing copywriter that creates engaging product descriptions.",
    parameters=AiCallParameters(
        model="gpt-4o-mini",
        temperature=0.8,
    ),
)

ai_call = StructuredAiCall(
    ctx=ctx,
    config=config,
    formatter=auto_formatter_for_type(ProductInfo),
    parser=auto_parser_for_type(ProductDescription),
    retry_policy=None,
)
```

### Alternative: Load configuration from files

You can also load the system message and parameters from separate files:

```python
from pathlib import Path

# Create config files:
# - prompts/product_writer.txt (system message)
# - prompts/product_writer.json (AiCallParameters as JSON)

ai_call = StructuredAiCall.from_files(
    ctx=ctx,
    path=Path("prompts/product_writer"),
    formatter=auto_formatter_for_type(ProductInfo),
    parser=auto_parser_for_type(ProductDescription),
)
```

**Example files:**

`prompts/product_writer.txt`:
```
You are a marketing copywriter that creates engaging product descriptions.
```

`prompts/product_writer.json`:
```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.8
}
```

## 5. Execute

```python
product = ProductInfo(
    name="Wireless Noise-Cancelling Headphones",
    category="Electronics",
    key_features=["Active noise cancellation", "30-hour battery", "Bluetooth 5.0"],
)
result = await ai_call(product)
print(f"Short: {result.short_description}")
print(f"Detailed: {result.detailed_description}")
print(f"Selling points: {result.selling_points}")
```

## What happens under the hood

1. **Formatting** — `ProductInfo` is converted to the appropriate format (JSON by default)
2. **API call** — Sent to OpenAI with the configured parameters
3. **Retry logic** — Network errors and validation failures are retried separately
4. **Parsing** — Response is validated against `ProductDescription` schema
5. **Result** — Typed, validated product description is returned

## Next steps

- [Formatters](formatters.md) — customize input formatting
- [Parsers](parsers.md) — customize response parsing
- [Retry policies](retry.md) — configure retry behavior
