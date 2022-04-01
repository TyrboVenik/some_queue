from typing import Optional

from pydantic import BaseModel


class RequestModel(BaseModel):
    data: str


class ResponseModel(BaseModel):
    id: int


class StatusModel(BaseModel):
    id: int
    status: Optional[int]


class QueueMessage(BaseModel):
    id: int
    data: str
