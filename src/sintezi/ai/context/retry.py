import sys

import tenacity.wait
from pydantic import BaseModel


class RetryParameters(BaseModel):
    stop_after_attempt: int | None = None
    stop_after_delay: float | None = None

    wait_initial: float | None = None
    wait_max: float | None = None

    def merge(self, child: "RetryParameters | None") -> "RetryParameters":
        if not child:
            return self
        overrides = child.model_dump(exclude_none=True)
        return self.model_copy(update=overrides)

    def to_wait(self) -> tenacity.wait.wait_base:
        wait_initial = self.wait_initial or 0
        wait_max = self.wait_max or sys.maxsize / 2

        return tenacity.wait_exponential_jitter(initial=wait_initial, max=wait_max)

    def to_stop(self) -> tenacity.stop.stop_base:
        if self.stop_after_attempt:
            stop_attempts = tenacity.stop_after_attempt(self.stop_after_attempt)
        else:
            stop_attempts = None

        if self.stop_after_delay:
            stop_delay = tenacity.stop_after_delay(self.stop_after_delay)
        else:
            stop_delay = None

        return tenacity.stop_any(*(x for x in (stop_attempts, stop_delay) if x is not None))


class RetryPolicy(BaseModel):
    network: RetryParameters | None = None
    validation: RetryParameters | None = None

    def merge(self, child: "RetryPolicy | None") -> "RetryPolicy":
        if not child:
            return self

        return RetryPolicy(
            network=self.network.merge(child.network) if self.network is not None else child.network,
            validation=self.validation.merge(child.validation) if self.validation is not None else child.validation,
        )
