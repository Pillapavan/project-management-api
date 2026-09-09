from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.security.auth import get_current_user
from app.services.project_service import create_new_project,add_member_to_project,get_project_members_for_user,remove_member_from_project,get_all_projects
from app.schemas.project_member import ProjectMemberResponse,ProjectMemberDetailResponse


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project_endpoint(
    project_data: ProjectCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_project(
        db=db,
        name=project_data.name,
        description=project_data.description,
        current_user=current_user
    )

@router.post(
    "/{project_id}/members/{user_id}",
    response_model=ProjectMemberResponse,
    status_code=status.HTTP_201_CREATED
)
def add_member(
    project_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_member_to_project(
        db=db,
        project_id=project_id,
        user_id=user_id,
        current_user=current_user
    )


@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMemberDetailResponse]
)
def get_members(
    project_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_project_members_for_user(
        db=db,
        project_id=project_id,
        current_user=current_user
    )

@router.delete("/{project_id}/members/{user_id}")
def remove_member(
    project_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return remove_member_from_project(
        db=db,
        project_id=project_id,
        user_id=user_id,
        current_user=current_user
    )


@router.get(
    "/projects",
    response_model=list[ProjectResponse]
)
def list_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_projects(
        db=db,
        page=page,
        limit=limit
    )