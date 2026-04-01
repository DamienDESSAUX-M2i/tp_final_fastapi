from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate


def get_player_by_nickname(db: Session, nickname: str) -> Optional[Player]:
    """Recherche un joueur par son nickname"""
    return db.query(Player).filter(Player.nickname == nickname).first()


def get_player_by_id(db: Session, player_id: int) -> Optional[Player]:
    """Recherche un joueur par son identifiant"""
    return db.query(Player).filter(Player.id == player_id).first()


def get_all_players(db: Session) -> List[Player]:
    """Retourne tous les joueurs triés par identifiant"""
    return db.query(Player).order_by(Player.id.asc()).all()


def create_player(db: Session, player_in: PlayerCreate) -> Player:
    """
    Crée un joueur en base.
    """

    existing_player = get_player_by_nickname(db, player_in.nickname)
    if existing_player:
        raise ValueError("Nickname already exists")

    player = Player(**player_in.model_dump())

    db.add(player)
    db.commit()
    db.refresh(player)

    return player


def update_player(
    db: Session,
    player_id: int,
    player_in: PlayerUpdate,
) -> Optional[Player]:
    """
    Met à jour un joueur existant.
    """

    player = get_player_by_id(db, player_id)
    if not player:
        return None

    update_data = player_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(player, field, value)

    db.commit()
    db.refresh(player)

    return player


def delete_player_by_id(db: Session, player_id: int) -> Optional[Player]:
    """
    Supprime un joueur s'il existe.
    """
    player = get_player_by_id(db, player_id)
    if not player:
        return None

    db.delete(player)
    db.commit()

    return player
