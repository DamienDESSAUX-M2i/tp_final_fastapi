from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from app.schemas.utils import APIResponse, MessageResponse
from app.services.player import (
    create_player,
    delete_player_by_id,
    get_all_players,
    get_player_by_id,
    get_player_by_nickname,
)

router = APIRouter(prefix="/private", tags=["PLayer"])


@router.get("/players/", response_model=APIResponse[List[PlayerRead]])
def list_players(
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[List[PlayerRead]]:
    """Liste tous les joueurs (accessible aux users et admins)."""
    players = get_all_players(db)
    players_data = [PlayerRead(id=p.id, nickname=p.nickname) for p in players]
    return APIResponse(
        status=True,
        data=players_data,
        message=f"{len(players_data)} joueurs trouvés.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/players/{player_id}", response_model=APIResponse[PlayerRead])
def get_player(
    player_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[PlayerRead]:
    """Récupère un joueur par son identifiant."""
    player = get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur {player_id} introuvable.",
        )
    return APIResponse(
        status=True,
        data=PlayerRead(id=player.id, nickname=player.nickname),
        message="Joueur récupéré avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/players/by-nickname/{nickname}", response_model=APIResponse[PlayerRead])
def get_player_nickname(
    nickname: str,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[PlayerRead]:
    """Récupère un joueur par son nickname."""
    player = get_player_by_nickname(db, nickname)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur avec nickname '{nickname}' introuvable.",
        )
    return APIResponse(
        status=True,
        data=PlayerRead(id=player.id, nickname=player.nickname),
        message="Joueur récupéré avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.post(
    "/players/",
    response_model=APIResponse[PlayerRead],
    status_code=status.HTTP_201_CREATED,
)
def create_new_player(
    player_in: PlayerCreate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[PlayerRead]:
    """Crée un nouveau joueur."""
    existing_player = get_player_by_nickname(db, player_in.nickname)
    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce nom de joueur existe déjà.",
        )

    player = create_player(db, player_in)
    return APIResponse(
        status=True,
        data=PlayerRead(id=player.id, nickname=player.nickname),
        message="Joueur créé avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.put("/players/{player_id}", response_model=APIResponse[PlayerRead])
def update_player(
    player_id: int,
    player_in: PlayerUpdate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[PlayerRead]:
    """Met à jour un joueur existant."""
    existing_player = get_player_by_nickname(db, player_in.nickname)
    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce nom de joueur existe déjà.",
        )

    player = get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur {player_id} introuvable.",
        )

    if player_in.nickname:
        player.nickname = player_in.nickname

    db.commit()
    db.refresh(player)

    return APIResponse(
        status=True,
        data=PlayerRead(id=player.id, nickname=player.nickname),
        message="Joueur mis à jour avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/players/{player_id}", response_model=APIResponse[MessageResponse])
def delete_player(
    player_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MessageResponse]:
    """Supprime un joueur."""
    deleted_player = delete_player_by_id(db, player_id)
    if not deleted_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Joueur {player_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=MessageResponse(message=f"Joueur '{deleted_player.nickname}' supprimé."),
        message="Suppression réussie.",
        timestamp=datetime.now(timezone.utc),
    )
