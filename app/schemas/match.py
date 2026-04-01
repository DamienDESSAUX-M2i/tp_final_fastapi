from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class MatchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    date: datetime
    team_one_id: int
    team_two_id: int


class MatchCreate(MatchBase):
    @model_validator(mode="after")
    def validate_teams(self):
        if self.team_one_id == self.team_two_id:
            raise ValueError("Teams must be different")

        if self.team_one_id > self.team_two_id:
            raise ValueError("team_one_id must be < team_two_id")

        return self


class MatchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime]
    team_one_id: Optional[int]
    team_two_id: Optional[int]

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team_one_id is not None and self.team_two_id is not None:
            if self.team_one_id == self.team_two_id:
                raise ValueError("Teams must be different")

            if self.team_one_id > self.team_two_id:
                raise ValueError("team_one_id must be < team_two_id")

        return self


class MatchRead(MatchBase):
    id: int

    class Config:
        from_attributes = True
