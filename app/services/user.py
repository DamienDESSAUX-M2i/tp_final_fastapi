from typing import Optional

from app.core.security import hash_password
from app.models.user import User, UserRole
from sqlalchemy.orm import Session


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Recherche un utilisateur par son nom d'utilisateur"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Recherche un utilisateur par son identifiant"""
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session) -> list[User]:
    """Retourne tous les utilisateurs triés par identifiant"""
    return db.query(User).order_by(User.id.asc()).all()


def create_user(
    db: Session,
    username: str,
    full_name: str,
    password: str,
    role: UserRole | str = UserRole.USER.value,
    is_active: bool = True,
) -> User:
    """
    Crée un utilisateur en base.
    Le mot de passe est hashé avant l'insertion.
    """
    password_hash = hash_password(password)

    user = User(
        username=username,
        full_name=full_name,
        password_hash=password_hash,
        role=role.value if isinstance(role, UserRole) else role,
        is_active=is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Supprime un utilisateur s'il existe.
    Retourne l'utilisateur supprimé ou None.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user
