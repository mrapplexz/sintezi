import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Self, TypeVar, cast

import tenacity
from openai import OpenAIError
from openai.types.chat.completion_create_params import ResponseFormat

from sintezi.ai.context import AiContext, RetryPolicy
from sintezi.ai.formatter import RequestFormatter
from sintezi.ai.parser import ResponseParser

from .params import AiCallParameters

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

_LOGGER = logging.getLogger(__name__)


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
        retry_policy: RetryPolicy | None,
    ) -> None:
        self._ctx = ctx
        self._config = config
        self._formatter = formatter
        self._parser = parser

        retry_policy = self._ctx.retry_policy.merge(retry_policy)
        retry_policy_validation = retry_policy.validation
        retry_policy_network = retry_policy.network
        if retry_policy_validation is None:
            raise ValueError("No validation retry policy")
        if retry_policy_network is None:
            raise ValueError("No network retry policy")
        self._retry_policy_validation = retry_policy_validation
        self._retry_policy_network = retry_policy_network

    async def __call__(self, inputs: TRequest) -> TResponse:
        response_format = cast(
            ResponseFormat, self._parser.to_response_format(capabilities=self._ctx.response_format_capabilities)
        )

        @tenacity.retry(
            stop=self._retry_policy_validation.to_stop(),
            wait=self._retry_policy_validation.to_wait(),
            retry=tenacity.retry_if_exception_type(ValueError),
            reraise=True,
            before_sleep=tenacity.before_log(_LOGGER, log_level=logging.WARNING),
        )
        @tenacity.retry(
            stop=self._retry_policy_network.to_stop(),
            wait=self._retry_policy_network.to_wait(),
            retry=tenacity.retry_if_exception_type((OSError, OpenAIError)),
            reraise=True,
            before_sleep=tenacity.before_log(_LOGGER, log_level=logging.WARNING),
        )
        async def run_with_retry() -> TResponse:
            result = await self._ctx.async_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self._config.system_message},
                    {"role": "user", "content": self._formatter.format(inputs)},
                ],
                response_format=response_format,
                model=self._config.parameters.model,
                temperature=self._config.parameters.temperature,
            )
            if not result.choices:
                exc = ValueError("Got no choices from AI provider")
                exc.add_note(str(result))
                raise exc

            message = result.choices[0].message

            if message is None:
                exc = ValueError("Got no message from AI provider")
                exc.add_note(str(result))
                raise exc

            content = message.content

            if content is None:
                exc = ValueError("Got empty content from AI provider")
                exc.add_note(str(result))
                raise exc

            return self._parser.validate(content)

        return await run_with_retry()

    @classmethod
    def from_files(
        cls,
        ctx: AiContext,
        path: Path,
        formatter: RequestFormatter[TRequest],
        parser: ResponseParser[TResponse],
        retry_policy: RetryPolicy | None = None,
    ) -> Self:
        system_message = path.with_suffix(".txt").read_text(encoding="utf-8").strip()
        parameters = AiCallParameters.model_validate_json(path.with_suffix(".json").read_text(encoding="utf-8"))
        config = StructuredAiCallConfig(system_message=system_message, parameters=parameters)
        return cls(ctx, config, formatter=formatter, parser=parser, retry_policy=retry_policy)
