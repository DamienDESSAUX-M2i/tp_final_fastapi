from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base
from app.models.team import Team


class Match(Base):
    __tablename__ = "matches"

    __table_args__ = (
        CheckConstraint(
            "team_one_id <> team_two_id",
            name="check_teams_different",
        ),
        CheckConstraint(
            "team_one_id < team_two_id",
            name="check_team_order",
        ),
        UniqueConstraint(
            "team_one_id",
            "team_two_id",
            "date",
            name="unique_match",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    place: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    team_one_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    team_two_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
    )

    team_one: Mapped[Team] = relationship(foreign_keys=[team_one_id])
    team_two: Mapped[Team] = relationship(foreign_keys=[team_two_id])
