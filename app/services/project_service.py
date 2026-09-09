from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.project_repository import create_project,get_project_by_id,get_project_member,add_project_member,get_project_members,delete_project_member,get_projects
from app.repositories.user_repository import get_user_by_id


def create_new_project(
    db: Session,
    name: str,
    description: str | None,
    current_user: User
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or manager can create a project"
        )

    project = create_project(
        db=db,
        name=name,
        description=description,
        created_by=current_user.id
    )

    return project


def add_member_to_project(
    db: Session,
    project_id: int,
    user_id: int,
    current_user: User
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or manager can add project members"
        )

    project = get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    existing_member = get_project_member(
        db,
        project_id,
        user_id
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a project member"
        )

    return add_project_member(
        db=db,
        project_id=project_id,
        user_id=user_id
    )


def get_project_members_for_user(
    db: Session,
    project_id: int,
    current_user: User
):
    project = get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if current_user.role in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        return get_project_members(db, project_id)

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

    return get_project_members(db, project_id)


def remove_member_from_project(
    db: Session,
    project_id: int,
    user_id: int,
    current_user: User
):
    if current_user.role not in {
        UserRole.ADMIN,
        UserRole.MANAGER
    }:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or manager can remove project members"
        )

    project = get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    membership = get_project_member(
        db,
        project_id,
        user_id
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a member of this project"
        )

    delete_project_member(db, membership)

    return {
        "message": "Member removed successfully"
    }


def get_all_projects(
    db: Session,
    page: int,
    limit: int
):
    offset = (page - 1) * limit

    return get_projects(
        db=db,
        offset=offset,
        limit=limit
    )