from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str
):
    statement = select(User).where(User.email == email)

    return db.scalars(statement).first()


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(db: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    return db.scalars(statement).first()