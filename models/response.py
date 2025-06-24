from pydantic import BaseModel


class Model(BaseModel):
    name: str
    provider: str
    version: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponseData(BaseModel):
    result: str
    model: Model
    usage: Usage


class ChatResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: ChatResponseData
    request_id: str
    timestamp: int


class ErrorResponse(BaseModel):
    code: int
    message: str
    request_id: str
    timestamp: int
