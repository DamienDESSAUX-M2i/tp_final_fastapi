from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base
from app.models.player import Player


class Team(Base):
    __tablename__ = "teams"

    __table_args__ = (
        CheckConstraint(
            "player_one_id <> player_two_id",
            name="check_players_different",
        ),
        CheckConstraint(
            "player_one_id < player_two_id",
            name="check_player_order",
        ),
        UniqueConstraint(
            "player_one_id",
            "player_two_id",
            name="unique_team_players",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    player_one_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
    )
    player_two_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
    )

    player_one: Mapped[Player] = relationship(foreign_keys=[player_one_id])
    player_two: Mapped[Player] = relationship(foreign_keys=[player_two_id])
