# Parsers

Parsers validate and convert LLM responses back into structured objects.

## Auto-detection

Use `auto_parser_for_type` to automatically select the right parser:

```python
from sintezi.ai.parser import auto_parser_for_type

parser = auto_parser_for_type(MyResponseModel)
```

This automatically selects the best parser based on your model structure:

- For regular Pydantic `BaseModel` classes, it uses **JSON** parser
- For `pydantic-xml` `BaseXmlModel` classes, it uses **XML** parser
- For plain `str` types, it returns the response as-is

## Available parsers

### JSON

```python
from sintezi.ai.parser import JsonParser, JsonResponseFormat

parser = JsonParser(model_type=MyResponseModel, response_format=JsonResponseFormat.json_schema)
```

Works with OpenAI's `response_format` for structured outputs.

### XML

```python
from sintezi.ai.parser import XmlParser

parser = XmlParser(model_type=MyResponseModel)
```

Requires `pydantic-xml`.

### Plain text

```python
from sintezi.ai.parser import StrParser

parser = StrParser()
```

For simple string responses.

## Validation

All parsers automatically validate responses against your Pydantic schema. If validation fails, a `ValueError` is raised and the retry policy handles it.

## Custom parsers

Implement `ResponseParser[T]`:

```python
from sintezi.ai.parser import ResponseParser, ResponseFormatCapability
from typing import TypeVar

T = TypeVar("T")

class MyCustomParser(ResponseParser[str]):
    @property
    def returns(self) -> type[str]:
        return str

    def validate(self, content: str) -> str:
        return content.strip()

    def to_response_format(self, capabilities: set[ResponseFormatCapability]) -> dict | None:
        return None
```

## Next steps

- [Formatters](formatters.md) — input formatting
- [Retry policies](retry.md) — handling validation failures
