from pydantic import BaseModel, Field


class PlayerDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
