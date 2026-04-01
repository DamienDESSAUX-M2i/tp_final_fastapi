from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team
from app.schemas.match import MatchCreate, MatchUpdate


def get_match_by_id(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.id == match_id).first()


def get_all_matches(db: Session) -> List[Match]:
    return db.query(Match).order_by(Match.date.desc()).all()


def get_match_by_teams_place_date(
    db: Session,
    place: str,
    team_one_id: int,
    team_two_id: int,
    date: datetime,
) -> Optional[Match]:
    return (
        db.query(Match)
        .filter(
            Match.place == place,
            Match.team_one_id == team_one_id,
            Match.team_two_id == team_two_id,
            Match.date == date,
        )
        .first()
    )


def validate_match(db: Session, team_one_id: int, team_two_id: int):
    if team_one_id == team_two_id:
        raise ValueError("Teams must be different")

    if team_one_id > team_two_id:
        team_one_id, team_two_id = team_two_id, team_one_id

    team_one = db.get(Team, team_one_id)
    team_two = db.get(Team, team_two_id)

    if not team_one or not team_two:
        raise ValueError("One or both teams do not exist")

    players = {
        team_one.player_one_id,
        team_one.player_two_id,
        team_two.player_one_id,
        team_two.player_two_id,
    }

    if len(players) != 4:
        raise ValueError("All 4 players must be different")

    return team_one_id, team_two_id


def create_match(db: Session, match_in: MatchCreate) -> Match:
    """
    Crée un match avec validation complète.
    """

    t1, t2 = validate_match(db, match_in.team_one_id, match_in.team_two_id)

    existing_match = get_match_by_teams_place_date(
        db, match_in.place, t1, t2, match_in.date
    )
    if existing_match:
        raise ValueError("Match already exists for these teams at this date")

    match = Match(
        place=match_in.place,
        date=match_in.date,
        team_one_id=t1,
        team_two_id=t2,
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def update_match(
    db: Session,
    match_id: int,
    match_in: MatchUpdate,
) -> Optional[Match]:

    match = get_match_by_id(db, match_id)
    if not match:
        return None

    update_data = match_in.model_dump(exclude_unset=True)

    t1 = update_data.get("team_one_id", match.team_one_id)
    t2 = update_data.get("team_two_id", match.team_two_id)

    t1, t2 = validate_match(db, t1, t2)

    place = update_data.get("place", match.place)
    date = update_data.get("date", match.date)

    existing_match = get_match_by_teams_place_date(db, place, t1, t2, date)
    if existing_match and existing_match.id != match_id:
        raise ValueError("Another match already exists with same teams and date")

    match.place = place
    match.team_one_id = t1
    match.team_two_id = t2
    match.date = date

    db.commit()
    db.refresh(match)

    return match


def delete_match(db: Session, match_id: int) -> Optional[Match]:
    match = get_match_by_id(db, match_id)
    if not match:
        return None

    db.delete(match)
    db.commit()

    return match
