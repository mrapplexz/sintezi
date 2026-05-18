# Formatters

Formatters convert your structured objects into LLM-readable text formats.

## Auto-detection

The easiest way is to use `auto_formatter_for_type`:

```python
from sintezi.ai.formatter import auto_formatter_for_type

formatter = auto_formatter_for_type(MyModel)
```

This automatically selects the best formatter based on your model structure:

- For regular Pydantic `BaseModel` classes, it uses **JSON** formatter
- For `pydantic-xml` `BaseXmlModel` classes, it uses **XML** formatter
- For plain `str` types, it passes them through directly

## Available formatters

### JSON

```python
from sintezi.ai.formatter import JsonFormatter

formatter = JsonFormatter(model=MyModel)
```

Most compatible with OpenAI's structured output format.

### XML

```python
from sintezi.ai.formatter import XmlFormatter

formatter = XmlFormatter(model=MyModel)
```

Requires `pydantic-xml`. Useful for complex nested structures.

### Plain text

```python
from sintezi.ai.formatter import StrFormatter

formatter = StrFormatter(model=str)
```

For simple string-based inputs.

## Custom formatters

Implement `RequestFormatter[T]`:

```python
from sintezi.ai.formatter import RequestFormatter
from typing import TypeVar

T = TypeVar("T")

class MyCustomFormatter(RequestFormatter[T]):
    def format(self, data: T) -> str:
        # Convert data to string format
        return str(data)
```

## Next steps

- [Parsers](parsers.md) — parsing LLM responses
- [API Reference](../reference/index.md) — complete formatter API
