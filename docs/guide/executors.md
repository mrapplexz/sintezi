# Executors

Executors are the main interface for generating synthetic data with sintezi. They orchestrate formatting, API calls, parsing, and retry logic.

## Available executors

### StructuredAiCall

The primary executor for generating structured synthetic data from typed inputs to typed outputs.

```python
from sintezi.ai.executor import StructuredAiCall, StructuredAiCallConfig, AiCallParameters
from sintezi.ai.formatter import auto_formatter_for_type
from sintezi.ai.parser import auto_parser_for_type

config = StructuredAiCallConfig(
    system_message="Your system prompt here",
    parameters=AiCallParameters(
        model="gpt-4o-mini",
        temperature=0.7,
    ),
)

ai_call = StructuredAiCall(
    ctx=ctx,
    config=config,
    formatter=auto_formatter_for_type(InputModel),
    parser=auto_parser_for_type(OutputModel),
    retry_policy=None,
)

result = await ai_call(input_data)
```

**Key features:**

- Type-safe input and output with Pydantic models
- Automatic format selection (JSON, XML, plain text)
- Separate retry policies for network and validation errors
- Support for loading configuration from files

**Use cases:**

- Bulk synthetic data generation
- Data augmentation (paraphrasing, translation, expansion)
- Structured data transformation
- Test data generation

### Loading from files

Store prompts and parameters separately:

```python
from pathlib import Path

ai_call = StructuredAiCall.from_files(
    ctx=ctx,
    path=Path("prompts/my_prompt"),
    formatter=auto_formatter_for_type(InputModel),
    parser=auto_parser_for_type(OutputModel),
)
```

This expects:
- `prompts/my_prompt.txt` — system message
- `prompts/my_prompt.json` — `AiCallParameters` as JSON

## Future executors

More executors will be added in future versions:

- **Agent loop executor** — for multi-step agentic workflows with tool use
- **Batch executor** — for efficient bulk generation with OpenAI batch API
- **Streaming executor** — for real-time synthetic data generation

## Configuration

All executors share common configuration patterns:

### AiCallParameters

```python
from sintezi.ai.executor import AiCallParameters

params = AiCallParameters(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000,
    top_p=1.0,
)
```

### System messages

System messages define the LLM's behavior:

```python
config = StructuredAiCallConfig(
    system_message="You are a data generator that creates realistic synthetic examples.",
    parameters=params,
)
```

## Next steps

- [Formatters](formatters.md) — customize input formatting
- [Parsers](parsers.md) — customize response parsing
- [Retry policies](retry.md) — configure retry behavior
- [API Reference](../reference/index.md) — complete executor API
