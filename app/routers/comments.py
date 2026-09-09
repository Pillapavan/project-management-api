from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.comment import CommentCreate, CommentResponse,CommentUpdate
from app.security.auth import get_current_user
from app.services.comment_service import create_new_comment,get_issue_comments,update_existing_comment,delete_existing_comment


router = APIRouter(
    tags=["Comments"]
)


@router.post(
    "/issues/{issue_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment_endpoint(
    issue_id: int,
    comment_data: CommentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_comment(
        db=db,
        issue_id=issue_id,
        content=comment_data.content,
        current_user=current_user
    )

@router.get(
    "/issues/{issue_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments_endpoint(
    issue_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_issue_comments(
        db=db,
        issue_id=issue_id,
        current_user=current_user
    )

@router.put(
    "/comments/{comment_id}",
    response_model=CommentResponse
)
def update_comment_endpoint(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_existing_comment(
        db=db,
        comment_id=comment_id,
        content=comment_data.content,
        current_user=current_user
    )


@router.delete("/comments/{comment_id}")
def delete_comment_endpoint(
    comment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_existing_comment(
        db=db,
        comment_id=comment_id,
        current_user=current_user
    )