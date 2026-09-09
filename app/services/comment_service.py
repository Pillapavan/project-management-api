from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User,UserRole
from app.repositories.comment_repository import (
    create_comment,
    get_comments_by_issue,
    get_comment_by_id,
    update_comment,
    delete_comment,
)

from app.repositories.issue_repository import get_issue_by_id
from app.repositories.project_repository import get_project_member


def create_new_comment(
    db: Session,
    issue_id: int,
    content: str,
    current_user: User
):
    issue = get_issue_by_id(
        db=db,
        issue_id=issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    membership = get_project_member(
        db,
        issue.project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    return create_comment(
        db=db,
        issue_id=issue_id,
        user_id=current_user.id,
        content=content
    )

def get_issue_comments(
    db: Session,
    issue_id: int,
    current_user: User
):
    issue = get_issue_by_id(
        db=db,
        issue_id=issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    membership = get_project_member(
        db,
        issue.project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    return get_comments_by_issue(
        db=db,
        issue_id=issue_id
    )


def update_existing_comment(
    db: Session,
    comment_id: int,
    content: str,
    current_user: User
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    issue = get_issue_by_id(
        db=db,
        issue_id=comment.issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    membership = get_project_member(
        db,
        issue.project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    is_author = comment.user_id == current_user.id

    is_manager_or_admin = current_user.role in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }

    if not is_author and not is_manager_or_admin:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments"
        )

    return update_comment(
        db=db,
        comment=comment,
        content=content
    )


def delete_existing_comment(
    db: Session,
    comment_id: int,
    current_user: User
):
    comment = get_comment_by_id(
        db=db,
        comment_id=comment_id
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    issue = get_issue_by_id(
        db=db,
        issue_id=comment.issue_id
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    membership = get_project_member(
        db,
        issue.project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    is_author = comment.user_id == current_user.id

    is_manager_or_admin = current_user.role in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }

    if not is_author and not is_manager_or_admin:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments"
        )

    delete_comment(
        db=db,
        comment=comment
    )

    return {
        "message": "Comment deleted successfully"
    }
