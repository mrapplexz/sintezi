# Retry policies

sintezi uses separate retry policies for network errors and validation failures.

## Default retry behavior

By default, sintezi retries:
- **Network errors** (OSError, OpenAIError) with exponential backoff
- **Validation errors** (ValueError) with exponential backoff

## Custom retry policies

```python
from sintezi.ai.context import RetryPolicy, RetryParameters

retry_policy = RetryPolicy(
    validation=RetryParameters(
        stop_after_attempt=5,       # Max 5 validation retries
        stop_after_delay=60.0,      # Or stop after 60 seconds
        wait_initial=1.0,           # Start with 1 second wait
        wait_max=10.0,              # Max 10 seconds between retries
    ),
    network=RetryParameters(
        stop_after_attempt=3,       # Max 3 network retries
        wait_initial=2.0,
        wait_max=30.0,
    ),
)
```

## Apply retry policy

### At context level (global)

```python
ctx = ai_context_from_openai(client, retry_policy=retry_policy)
```

All calls using this context inherit the retry policy.

### At call level (per-call override)

```python
ai_call = StructuredAiCall(
    ctx=ctx,
    config=config,
    formatter=formatter,
    parser=parser,
    retry_policy=retry_policy,  # Overrides context policy
)
```

## Retry parameters

| Parameter | Description |
|-----------|-------------|
| `stop_after_attempt` | Maximum number of retry attempts |
| `stop_after_delay` | Maximum total time for retries (seconds) |
| `wait_initial` | Initial wait time between retries (seconds) |
| `wait_max` | Maximum wait time between retries (seconds) |

Retry uses exponential backoff with jitter by default.

## Merging policies

Child policies override parent values:

```python
parent = RetryPolicy(
    validation=RetryParameters(stop_after_attempt=5),
)

child = RetryPolicy(
    validation=RetryParameters(stop_after_attempt=3),  # Overrides parent
)

merged = parent.merge(child)  # Uses stop_after_attempt=3
```

## Next steps

- [API Reference](../reference/index.md) — complete retry API
