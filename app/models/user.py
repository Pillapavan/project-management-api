import enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer,String,func,Enum as SqlEnum,DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.projectmember import ProjectMember
    from app.models.comment import Comment
    from app.models.issue import Issue


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"


class User(Base):
    __tablename__ = "users"

    id :Mapped[int] = mapped_column(Integer, 
                                    primary_key=True,
                                      index=True)
    name :Mapped[str] = mapped_column(String(50),
                                       nullable=False)
    email :Mapped[str] = mapped_column(String(100),
                                        unique=True,
                                        index=True,
                                        nullable=False)
    password :Mapped[str] = mapped_column(String(250),
                                          nullable=False)
    role :Mapped[UserRole] = mapped_column(SqlEnum(UserRole,
                                                   native_enum=False,
                                                   length=20),
                                            default=UserRole.MEMBER,
                                            nullable=False)

    created_at :Mapped[DateTime] = mapped_column(DateTime,
                                                 server_default=func.now()
                                                 ,nullable=False)

    # Relationships
    created_projects: Mapped[list["Project"]] = relationship(
        back_populates="creator"
    )

    project_memberships: Mapped[list["ProjectMember"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    created_issues: Mapped[list["Issue"]] = relationship(
        back_populates="creator",
        foreign_keys="Issue.created_by"
    )

    assigned_issues: Mapped[list["Issue"]] = relationship(
        back_populates="assignee",
        foreign_keys="Issue.assigned_to"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author"
    )


# User
#  ├── created_projects
#  ├── project_memberships
#  ├── created_issues
#  ├── assigned_issues
#  └── comments