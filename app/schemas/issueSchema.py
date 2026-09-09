from pydantic import BaseModel, ConfigDict, Field

from app.models.issue import IssuePriority, IssueStatus


class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    priority: IssuePriority = IssuePriority.MEDIUM


class IssueUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = None
    status: IssueStatus | None = None
    priority: IssuePriority | None = None


class IssueResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: IssueStatus
    priority: IssuePriority
    created_by: int
    assigned_to: int | None

    model_config = ConfigDict(from_attributes=True)