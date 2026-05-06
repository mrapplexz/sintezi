from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Self, TypeVar, cast

from openai.types.chat.completion_create_params import ResponseFormat

from sintezi.ai.context import AiContext
from sintezi.ai.formatter import RequestFormatter
from sintezi.ai.parser import ResponseParser

from .params import AiCallParameters

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


@dataclass
class StructuredAiCallConfig:
    system_message: str
    parameters: AiCallParameters


class StructuredAiCall(Generic[TRequest, TResponse]):
    def __init__(
        self,
        ctx: AiContext,
        config: StructuredAiCallConfig,
        formatter: RequestFormatter[TRequest],
        parser: ResponseParser[TResponse],
    ) -> None:
        self._ctx = ctx
        self._config = config
        self._formatter = formatter
        self._parser = parser

    async def __call__(self, inputs: TRequest) -> TResponse:
        response_format = cast(
            ResponseFormat, self._parser.to_response_format(capabilities=self._ctx.response_format_capabilities)
        )
        result = await self._ctx.async_client.chat.completions.create(
            messages=[
                {"role": "system", "content": self._config.system_message},
                {"role": "user", "content": self._formatter.format(inputs)},
            ],
            response_format=response_format,
            model=self._config.parameters.model,
            temperature=self._config.parameters.temperature,
        )
        content = result.choices[0].message.content

        if content is None:
            exc = ValueError("Got empty content from AI provider")
            exc.add_note(str(content))
            raise exc

        return self._parser.validate(content)

    @classmethod
    def from_files(
        cls, ctx: AiContext, path: Path, formatter: RequestFormatter[TRequest], parser: ResponseParser[TResponse]
    ) -> Self:
        system_message = path.with_suffix(".txt").read_text(encoding="utf-8").strip()
        parameters = AiCallParameters.model_validate_json(path.with_suffix(".json").read_text(encoding="utf-8"))
        config = StructuredAiCallConfig(system_message=system_message, parameters=parameters)
        return cls(ctx, config, formatter=formatter, parser=parser)
