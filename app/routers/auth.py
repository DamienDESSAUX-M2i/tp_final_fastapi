from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.dependencies.auth import get_current_user
from app.models.user import User, UserRole
from app.schemas.user import (
    LoginResponse,
    UserLogin,
    UserPublic,
    UserRegister,
)
from app.services.user import create_user, get_user_by_username

router = APIRouter(prefix="/auth", tags=["Authentication"])


def generate_access_token(user: User) -> str:
    """Génère un JWT à partir d'une instance de User"""
    return create_access_token(
        data={
            "sub": user.username,
            "role": user.role.value,
        },
    )


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> UserPublic:
    """Créer un nouvel utilisateur"""
    existing_user = get_user_by_username(db, payload.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce nom d'utilisateur existe déjà.",
        )

    created_user = create_user(
        db=db,
        username=payload.username,
        full_name=payload.full_name,
        password=payload.password,
        role=UserRole.USER,
    )

    return created_user


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
    """Authentifie l'utilisateur et retourne un JWT si valide"""
    settings = get_settings()

    user = get_user_by_username(db, payload.username)

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides."
        )

    access_token = generate_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes,
        "user": user,
    }


@router.post("/refresh", response_model=LoginResponse)
def refresh(current_user: User = Depends(get_current_user)) -> LoginResponse:
    """Génère un nouveau token pour l'utilisateur authentifié"""
    settings = get_settings()

    access_token = generate_access_token(current_user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes,
        "user": current_user,
    }
