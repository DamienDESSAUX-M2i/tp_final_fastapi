from typing import Optional

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=1, max_length=50)


class PlayerRead(PlayerBase):
    id: int

    class Config:
        from_attributes = True
