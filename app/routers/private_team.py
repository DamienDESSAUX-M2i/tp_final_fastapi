from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.schemas.utils import APIResponse, MessageResponse
from app.services.team import (
    create_team,
    delete_team,
    get_all_teams,
    get_team_by_id,
    get_team_by_name,
    update_team,
)

router = APIRouter(prefix="/private", tags=["Private"])


@router.get("/teams/", response_model=APIResponse[List[TeamRead]])
def list_teams(
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[List[TeamRead]]:
    """Liste toutes les équipes."""
    teams = get_all_teams(db)
    teams_data = [
        TeamRead(
            id=t.id,
            name=t.name,
            player_one_id=t.player_one_id,
            player_two_id=t.player_two_id,
        )
        for t in teams
    ]
    return APIResponse(
        status=True,
        data=teams_data,
        message=f"{len(teams_data)} équipes trouvées.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/teams/{team_id}", response_model=APIResponse[TeamRead])
def get_team(
    team_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[TeamRead]:
    """Récupère une équipe par son identifiant."""
    team = get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Équipe {team_id} introuvable.",
        )
    return APIResponse(
        status=True,
        data=TeamRead(
            id=team.id,
            name=team.name,
            player_one_id=team.player_one_id,
            player_two_id=team.player_two_id,
        ),
        message="Équipe récupérée avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/teams/by-name/{name}", response_model=APIResponse[TeamRead])
def get_team_name(
    name: str,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[TeamRead]:
    """Récupère une équipe par son nom (unique)."""
    team = get_team_by_name(db, name)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Équipe avec nom '{name}' introuvable.",
        )
    return APIResponse(
        status=True,
        data=TeamRead(
            id=team.id,
            name=team.name,
            player_one_id=team.player_one_id,
            player_two_id=team.player_two_id,
        ),
        message="Équipe récupérée avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.post(
    "/teams/",
    response_model=APIResponse[TeamRead],
    status_code=status.HTTP_201_CREATED,
)
def create_new_team(
    team_in: TeamCreate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[TeamRead]:
    """Crée une nouvelle équipe."""
    team = create_team(db, team_in)
    return APIResponse(
        status=True,
        data=TeamRead(
            id=team.id,
            name=team.name,
            player_one_id=team.player_one_id,
            player_two_id=team.player_two_id,
        ),
        message="Équipe créée avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.put("/teams/{team_id}", response_model=APIResponse[TeamRead])
def update_team_route(
    team_id: int,
    team_in: TeamUpdate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[TeamRead]:
    """Met à jour une équipe existante."""
    team = update_team(db, team_id, team_in)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Équipe {team_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=TeamRead(
            id=team.id,
            name=team.name,
            player_one_id=team.player_one_id,
            player_two_id=team.player_two_id,
        ),
        message="Équipe mise à jour avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/teams/{team_id}", response_model=APIResponse[MessageResponse])
def delete_team_route(
    team_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MessageResponse]:
    """Supprime une équipe."""
    deleted_team = delete_team(db, team_id)
    if not deleted_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Équipe {team_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=MessageResponse(message=f"Équipe '{deleted_team.name}' supprimée."),
        message="Suppression réussie.",
        timestamp=datetime.now(timezone.utc),
    )
