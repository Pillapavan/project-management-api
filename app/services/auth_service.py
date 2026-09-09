from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.security.password import hash_password,verify_password
from app.security.jwt import create_access_token


def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(password)

    user = create_user(
        db=db,
        name=name,
        email=email,
        password=hashed_password
    )

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    token = create_access_token(user.id)

    return token