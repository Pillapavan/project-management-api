from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.user import User,UserRole
from app.repositories.issue_repository import (
    create_issue,get_issue_by_id,get_issues_by_project,update_issue,delete_issue,assign_issue
)
from app.repositories.project_repository import (
    get_project_by_id,
    get_project_member,
)


def create_new_issue(
    db: Session,
    project_id: int,
    title: str,
    description: str | None,
    priority,
    current_user: User
):
    project = get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    membership = get_project_member(
        db,
        project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )

    return create_issue(
        db=db,
        project_id=project_id,
        title=title,
        description=description,
        priority=priority,
        created_by=current_user.id
    )

def get_project_issues(
    db: Session,
    project_id: int,
    current_user: User,
    status_filter=None,
    priority_filter=None,
    page: int = 1,
    limit: int = 20
):
    project = get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    membership = get_project_member(
        db,
        project_id,
        current_user.id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project"
        )

    offset = (page - 1) * limit

    return get_issues_by_project(
        db=db,
        project_id=project_id,
        status_filter=status_filter,
        priority_filter=priority_filter,
        offset=offset,
        limit=limit
    )


def get_issue_by_issueId(
    db: Session,
    issue_id : int,
    current_user: User
):
    
    issue = get_issue_by_id(db=db,issue_id=issue_id)

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )


    project = get_project_by_id(db, issue.project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
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

    return issue



def update_existing_issue(
    db: Session,
    issue_id: int,
    issue_data,
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

    project = get_project_by_id(
        db,
        issue.project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
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

    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=403,
            detail="Only admin or manager can update issues"
        )

    update_data = issue_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return update_issue(
        db=db,
        issue=issue,
        data=update_data
    )


def delete_existing_issue(
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

    project = get_project_by_id(
        db,
        issue.project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
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

    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=403,
            detail="Only admin or manager can delete issues"
        )

    delete_issue(
        db=db,
        issue=issue
    )

    return {
        "message": "Issue deleted successfully"
    }


def assign_issue_to_user(
    db: Session,
    issue_id: int,
    user_id: int,
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

    project = get_project_by_id(
        db,
        issue.project_id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=403,
            detail="Only admin or manager can assign issues"
        )

    target_membership = get_project_member(
        db,
        issue.project_id,
        user_id
    )

    if target_membership is None:
        raise HTTPException(
            status_code=400,
            detail="Assignee must be a member of the project"
        )

    return assign_issue(
        db=db,
        issue=issue,
        user_id=user_id
    )