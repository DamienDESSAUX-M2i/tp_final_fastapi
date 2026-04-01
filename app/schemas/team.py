from typing import Optional

from pydantic import BaseModel, Field, model_validator


class TeamBase(BaseModel):
    name: str = Field(..., max_length=50)
    player_one_id: int
    player_two_id: int


class TeamCreate(TeamBase):
    @model_validator(mode="after")
    def validate_players(self):
        if self.player_one_id == self.player_two_id:
            raise ValueError("Players must be different")

        if self.player_one_id > self.player_two_id:
            raise ValueError("player_one_id must be < player_two_id")

        return self


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    player_one_id: Optional[int]
    player_two_id: Optional[int]

    @model_validator(mode="after")
    def validate_players(self):
        if self.player_one_id is not None and self.player_two_id is not None:
            if self.player_one_id == self.player_two_id:
                raise ValueError("Players must be different")

            if self.player_one_id > self.player_two_id:
                raise ValueError("player_one_id must be < player_two_id")

        return self


class TeamRead(TeamBase):
    id: int

    class Config:
        from_attributes = True
