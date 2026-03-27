from typing import Dict, List

from pydantic import BaseModel


class PingResponse(BaseModel):
    message: str


class InfoResponse(BaseModel):
    message: str
    hint: str


class SecurityInfoResponse(BaseModel):
    authentication: str
    password_storage: str
    roles: List[str]
    public_endpoints: List[str]
    authenticated_endpoints: List[str]
    role_protected_endpoints: Dict[str, List[str]]


class RootResponse(BaseModel):
    message: str
    docs: str
    features: List[str]
