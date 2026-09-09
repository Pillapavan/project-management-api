from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.issueSchema import IssueCreate, IssueResponse,IssueUpdate
from app.security.auth import get_current_user
from app.services.issue_service import create_new_issue,get_project_issues,update_existing_issue,delete_existing_issue,assign_issue_to_user,get_issue_by_issueId
from app.models.issue import IssuePriority,IssueStatus

router = APIRouter(
    tags=["Issues"]
)


@router.post(
    "/projects/{project_id}/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED
)
def create_issue_endpoint(
    project_id: int,
    issue_data: IssueCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_new_issue(
        db=db,
        project_id=project_id,
        title=issue_data.title,
        description=issue_data.description,
        priority=issue_data.priority,
        current_user=current_user
    )


@router.get(
    "/projects/{project_id}/issues",
    response_model=list[IssueResponse]
)
@router.get(
    "/projects/{project_id}/issues",
    response_model=list[IssueResponse]
)
def get_project_issues_endpoint(
    project_id: int,
    status_filter: IssueStatus | None = Query(
        default=None,
        alias="status"
    ),
    priority_filter: IssuePriority | None = Query(
        default=None,
        alias="priority"
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_project_issues(
        db=db,
        project_id=project_id,
        current_user=current_user,
        status_filter=status_filter,
        priority_filter=priority_filter,
        page=page,
        limit=limit
    )

@router.get("/issues/{issue_id}",response_model=IssueResponse)
def get_issue_by_id(issue_id:int,    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)):
    return get_issue_by_issueId(issue_id=issue_id,db=db,current_user=current_user)



@router.put(
    "/issues/{issue_id}",
    response_model=IssueResponse
)
def update_issue_endpoint(
    issue_id: int,
    issue_data: IssueUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_existing_issue(
        db=db,
        issue_id=issue_id,
        issue_data=issue_data,
        current_user=current_user
    )


@router.delete("/issues/{issue_id}")
def delete_issue_endpoint(
    issue_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_existing_issue(
        db=db,
        issue_id=issue_id,
        current_user=current_user
    )


@router.post(
    "/issues/{issue_id}/assign/{user_id}",
    response_model=IssueResponse
)
def assign_issue_endpoint(
    issue_id: int,
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return assign_issue_to_user(
        db=db,
        issue_id=issue_id,
        user_id=user_id,
        current_user=current_user
    )