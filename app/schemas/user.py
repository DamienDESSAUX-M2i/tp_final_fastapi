from pydantic import BaseModel, ConfigDict, Field

from app.models import UserRole


class UserRegister(BaseModel):
    """Données attendues pour l'inscription d'un nouvel utilisateur."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    """Données attendues pour la connexion."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class UserPublic(BaseModel):
    """Représentation publique d'un utilisateur."""

    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Réponse renvoyée après un login ou un refresh."""

    access_token: str
    token_type: str = "bearer"


class LoginResponse(TokenResponse):
    """
    Variante enrichie de la réponse de login,
    incluant les informations publiques de l'utilisateur.
    """

    user: UserPublic
    expires_in: int = Field(..., gt=0)
