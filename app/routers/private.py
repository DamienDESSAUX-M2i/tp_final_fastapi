from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.player import PlayerDTO
from app.schemas.user import MessageResponse, UserPublic
from app.services.player import get_all_players
from app.services.user import delete_user_by_id, get_all_users

router = APIRouter(prefix="/private", tags=["Private"])


@router.get("/me", response_model=UserPublic)
def read_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    """Retourne les informations de l'utilisateur connecté."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }


@router.get("/users", response_model=List[UserPublic])
def list_users(
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER)),
    db: Session = Depends(get_db),
) -> List[UserPublic]:
    """Liste tous les utilisateurs pour admin ou user."""
    users = get_all_users(db)
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]


@router.get("/admin/users", response_model=List[UserPublic])
def admin_list_users(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> List[UserPublic]:
    """Liste tous les utilisateurs, réservé aux administrateurs."""
    users = get_all_users(db)
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]


@router.delete("/admin/users/{user_id}", response_model=MessageResponse)
def admin_delete_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Supprime un utilisateur par son identifiant (admin uniquement)."""
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrateur ne peut pas se supprimer lui-même.",
        )

    deleted_user = delete_user_by_id(db, user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return {"message": f"Utilisateur {deleted_user.username} supprimé."}


@router.get("/players", response_model=List[PlayerDTO])
def list_players(
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.USER)),
    db: Session = Depends(get_db),
) -> List[PlayerDTO]:
    """Liste tous les joueurs pour admin ou user."""
    players = get_all_players(db)
    return [
        {
            "id": player.id,
            "nickname": player.nickname,
        }
        for player in players
    ]
