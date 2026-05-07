from pydantic import BaseModel


class AiCallParameters(BaseModel):
    model: str
    temperature: float | None = None
