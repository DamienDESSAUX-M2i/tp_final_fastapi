from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


def get_team_by_id(db: Session, team_id: int) -> Optional[Team]:
    """Recherche une équipe par son id"""
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_name(db: Session, name: str) -> Optional[Team]:
    """Recherche une équipe par son nom"""
    return db.query(Team).filter(Team.name == name).first()


def get_all_teams(db: Session) -> List[Team]:
    """Retourne tous les équipes triés par identifiant"""
    return db.query(Team).order_by(Team.id.asc()).all()


def get_team_by_players(
    db: Session, player_one_id: int, player_two_id: int
) -> Optional[Team]:
    """Recherche une équipe par les id de ses joueurs"""
    return (
        db.query(Team)
        .filter(
            Team.player_one_id == player_one_id,
            Team.player_two_id == player_two_id,
        )
        .first()
    )


def validate_team(db: Session, player_one_id: int, player_two_id: int):
    """
    Validation métier
    """

    if player_one_id == player_two_id:
        raise ValueError("Players must be different")

    if player_one_id > player_two_id:
        player_one_id, player_two_id = player_two_id, player_one_id

    player_one = db.get(Player, player_one_id)
    if not player_one:
        raise ValueError("player with id {player_one_id} do not exist")

    player_two = db.get(Player, player_two_id)
    if not player_two:
        raise ValueError("player with id {player_two_id} do not exist")

    return player_one_id, player_two_id


def create_team(db: Session, team_in: TeamCreate) -> Team:
    """
    Crée une équipe avec validation métier.
    """

    if get_team_by_name(db, team_in.name):
        raise ValueError("Team name already exists")

    p1, p2 = validate_team(
        db,
        team_in.player_one_id,
        team_in.player_two_id,
    )

    existing_team = get_team_by_players(db, p1, p2)
    if existing_team:
        raise ValueError("Team already exists with these players")

    team = Team(
        name=team_in.name,
        player_one_id=p1,
        player_two_id=p2,
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


def update_team(
    db: Session,
    team_id: int,
    team_in: TeamUpdate,
) -> Optional[Team]:
    """
    Met à jour une équipe.
    """

    team = get_team_by_id(db, team_id)
    if not team:
        return None

    update_data = team_in.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_team = get_team_by_name(db, update_data["name"])
        if existing_team and existing_team.id != team_id:
            raise ValueError("Team name already exists")

        team.name = update_data["name"]

    if "player_one_id" in update_data or "player_two_id" in update_data:
        p1 = update_data.get("player_one_id", team.player_one_id)
        p2 = update_data.get("player_two_id", team.player_two_id)

        p1, p2 = validate_team(db, p1, p2)

        existing_team = get_team_by_players(db, p1, p2)
        if existing_team and existing_team.id != team_id:
            raise ValueError("Another team with same players exists")

        team.player_one_id = p1
        team.player_two_id = p2

    db.commit()
    db.refresh(team)

    return team


def delete_team(db: Session, team_id: int) -> Optional[Team]:
    """
    Supprime une équipe.
    """

    team = get_team_by_id(db, team_id)
    if not team:
        return None

    db.delete(team)
    db.commit()

    return team
