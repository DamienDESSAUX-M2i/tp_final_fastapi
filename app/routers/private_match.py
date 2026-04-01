from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.schemas.utils import APIResponse, MessageResponse
from app.services.match import (
    create_match,
    delete_match,
    get_all_matches,
    get_match_by_id,
    update_match,
)

router = APIRouter(prefix="/private", tags=["Match"])


@router.get("/matches/", response_model=APIResponse[List[MatchRead]])
def list_matches(
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[List[MatchRead]]:
    """Liste tous les matchs."""
    matches = get_all_matches(db)
    matches_data = [
        MatchRead(
            id=m.id,
            place=m.place,
            date=m.date,
            team_one_id=m.team_one_id,
            team_two_id=m.team_two_id,
        )
        for m in matches
    ]
    return APIResponse(
        status=True,
        data=matches_data,
        message=f"{len(matches_data)} matchs trouvés.",
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/matches/{match_id}", response_model=APIResponse[MatchRead])
def get_match(
    match_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MatchRead]:
    """Récupère un match par son identifiant."""
    match = get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=MatchRead(
            id=match.id,
            place=match.place,
            date=match.date,
            team_one_id=match.team_one_id,
            team_two_id=match.team_two_id,
        ),
        message="Match récupéré avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.post(
    "/matches/",
    response_model=APIResponse[MatchRead],
    status_code=status.HTTP_201_CREATED,
)
def create_new_match(
    match_in: MatchCreate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MatchRead]:
    """Crée un nouveau match."""
    match = create_match(db, match_in)
    return APIResponse(
        status=True,
        data=MatchRead(
            id=match.id,
            place=match.place,
            date=match.date,
            team_one_id=match.team_one_id,
            team_two_id=match.team_two_id,
        ),
        message="Match créé avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.put("/matches/{match_id}", response_model=APIResponse[MatchRead])
def update_match_route(
    match_id: int,
    match_in: MatchUpdate,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MatchRead]:
    """Met à jour un match existant."""
    match = update_match(db, match_id, match_in)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=MatchRead(
            id=match.id,
            place=match.place,
            date=match.date,
            team_one_id=match.team_one_id,
            team_two_id=match.team_two_id,
        ),
        message="Match mis à jour avec succès.",
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/matches/{match_id}", response_model=APIResponse[MessageResponse])
def delete_match_route(
    match_id: int,
    current_user: User = Depends(require_roles(UserRole.USER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> APIResponse[MessageResponse]:
    """Supprime un match."""
    deleted_match = delete_match(db, match_id)
    if not deleted_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} introuvable.",
        )

    return APIResponse(
        status=True,
        data=MessageResponse(message=f"Match '{deleted_match.place}' supprimé."),
        message="Suppression réussie.",
        timestamp=datetime.now(timezone.utc),
    )
