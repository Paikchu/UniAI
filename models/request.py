from typing import Optional

from pydantic import BaseModel, field_validator

from core.config import settings


class Parameters(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 100
    prompt_id: Optional[str] = None

    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        if v < 0.0 or v > 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    @field_validator('max_tokens')
    @classmethod
    def validate_max_tokens(cls, v):
        if v < 1 or v > 5000:
            raise ValueError("Max tokens must be between 1 and 5000")
        return v

    @field_validator('prompt_id')
    @classmethod
    def validate_prompt_id(cls, v):
        if v is not None and settings.get_prompt(v) is None:
            raise ValueError(f"Scene '{v}' not found")
        return v


class UserInfo(BaseModel):
    user_id: str
    user_role: str


class ChatRequest(BaseModel):
    model: str
    parameters: Parameters
    user_info: UserInfo
    request_id: str

    @field_validator('model')
    def validate_model(v):
        if hasattr(settings, 'models') and v not in settings.models:
            raise ValueError(f"Model '{v}' not found")
        return v
