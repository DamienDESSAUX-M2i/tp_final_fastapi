from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserPublic
from app.schemas.utils import APIResponse, MessageResponse
from app.services.user import delete_user_by_id, get_all_users

router = APIRouter(prefix="/private", tags=["User"])


@router.get("/me", response_model=APIResponse[UserPublic])
def read_me(current_user: User = Depends(get_current_user)) -> APIResponse[UserPublic]:
    """Retourne les informations de l'utilisateur connecté."""
    user_data = UserPublic(
        name=current_user.name,
        role=current_user.role,
        is_active=current_user.is_active,
    )
    return APIResponse(
        status=True,
        data=user_data,
        message="Utilisateur connecté récupéré avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/users", response_model=APIResponse[List[UserPublic]])
def list_users(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[List[UserPublic]]:
    """Liste tous les utilisateurs pour admin ou user."""
    users = get_all_users(db)
    users_data = [
        UserPublic(
            name=user.name,
            role=user.role,
            is_active=user.is_active,
        )
        for user in users
    ]
    return APIResponse(
        status=True,
        data=users_data,
        message=f"{len(users_data)} utilisateurs trouvés.",
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/users/{user_id}", response_model=APIResponse[MessageResponse])
def admin_delete_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MessageResponse]:
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

    return APIResponse(
        status=True,
        data=MessageResponse(message=f"Utilisateur {deleted_user.name} supprimé."),
        message="Utilisateur supprimé avec succès.",
        timestamp=datetime.now(timezone.utc),
    )
