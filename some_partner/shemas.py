from pydantic import BaseModel


class RequestModel(BaseModel):
    data: str


class ResponseModel(BaseModel):
    id: str


class StatusModel(BaseModel):
    id: str
    status: int
