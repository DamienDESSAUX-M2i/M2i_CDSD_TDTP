"""
Services d'accès aux utilisateurs via SQLAlchemy.

Le but de cette couche est de centraliser les opérations de base de données
plutôt que d'écrire les requêtes ORM directement dans les endpoints.
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User, UserRole


def get_user_by_username(db: Session, username: str):
    """
    Recherche un utilisateur par son nom d'utilisateur.
    Retourne un objet User ou None.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Recherche un utilisateur par son identifiant.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    """
    Retourne tous les utilisateurs triés par identifiant.
    """
    return db.query(User).order_by(User.id.asc()).all()


def create_user(db: Session, username: str, full_name: str, password: str, role: str = UserRole.USER.value):
    """
    Crée un utilisateur en base.

    Le mot de passe est hashé avant l'insertion.
    Le rôle par défaut d'un utilisateur inscrit est 'user'.
    """
    password_hash = hash_password(password)

    user = User(
        username=username,
        full_name=full_name,
        password_hash=password_hash,
        role=role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user_by_id(db: Session, user_id: int):
    """
    Supprime un utilisateur s'il existe.
    Retourne l'utilisateur supprimé ou None.
    """
    user = get_user_by_id(db, user_id)
    if user is None:
        return None

    db.delete(user)
    db.commit()
    return user
