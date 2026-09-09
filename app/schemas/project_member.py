from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectMemberResponse(BaseModel):
    project_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectMemberUserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberDetailResponse(BaseModel):
    user: ProjectMemberUserResponse
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)