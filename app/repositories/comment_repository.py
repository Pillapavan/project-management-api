from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment


def create_comment(
    db: Session,
    issue_id: int,
    user_id: int,
    content: str
):
    comment = Comment(
        issue_id=issue_id,
        user_id=user_id,
        content=content
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

def get_comments_by_issue(
    db: Session,
    issue_id: int
):
    statement = select(Comment).where(
        Comment.issue_id == issue_id
    )

    return db.scalars(statement).all()

def get_comment_by_id(
    db: Session,
    comment_id: int
):
    statement = select(Comment).where(
        Comment.id == comment_id
    )

    return db.scalars(statement).first()

def update_comment(
    db: Session,
    comment: Comment,
    content: str
):
    comment.content = content

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(
    db: Session,
    comment: Comment
):
    db.delete(comment)
    db.commit()