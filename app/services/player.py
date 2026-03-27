from typing import Optional

from app.models.player import PlayerDTO
from sqlalchemy.orm import Session


def get_player_by_nickname(db: Session, nickname: str) -> Optional[PlayerDTO]:
    """Recherche un joueur par son nom"""
    return db.query(PlayerDTO).filter(PlayerDTO.nickname == nickname).first()


def get_player_by_id(db: Session, players_id: int) -> Optional[PlayerDTO]:
    """Recherche un joueur par son identifiant"""
    return db.query(PlayerDTO).filter(PlayerDTO.id == players_id).first()


def get_all_players(db: Session) -> list[PlayerDTO]:
    """Retourne tous les joueurs triés par identifiant"""
    return db.query(PlayerDTO).order_by(PlayerDTO.id.asc()).all()


def create_player(
    db: Session,
    nickname: str,
) -> PlayerDTO:
    """
    Crée un joueur en base.
    """

    player = PlayerDTO(nickname=nickname)

    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def delete_player_by_id(db: Session, player_id: int) -> Optional[PlayerDTO]:
    """
    Supprime un utilisateur s'il existe.
    Retourne l'utilisateur supprimé ou None.
    """
    player = get_player_by_id(db, player_id)
    if not player:
        return None

    db.delete(player)
    db.commit()
    return player
