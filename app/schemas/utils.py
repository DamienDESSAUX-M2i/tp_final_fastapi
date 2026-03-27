from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    status: bool
    data: T
    message: str
    timestamp: datetime


class PingResponse(BaseModel):
    message: str


class InfoResponse(BaseModel):
    message: str
    hint: str


class SecurityInfoResponse(BaseModel):
    authentication: str
    password_storage: str
    roles: list[str]
    public_endpoints: list[str]
    authenticated_endpoints: list[str]
    role_protected_endpoints: dict[str, list[str]]


class RootResponse(BaseModel):
    message: str
    docs: str
    features: list[str]
