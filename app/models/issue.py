import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User
    from app.models.comment import Comment


class IssueStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class IssuePriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[IssueStatus] = mapped_column(
        SQLEnum(
            IssueStatus,
            native_enum=False,
            length=20
        ),
        default=IssueStatus.OPEN,
        nullable=False
    )

    priority: Mapped[IssuePriority] = mapped_column(
        SQLEnum(
            IssuePriority,
            native_enum=False,
            length=20
        ),
        default=IssuePriority.MEDIUM,
        nullable=False
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships

    project: Mapped["Project"] = relationship(
        back_populates="issues"
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_issues",
        foreign_keys=[created_by]
    )

    assignee: Mapped["User | None"] = relationship(
        back_populates="assigned_issues",
        foreign_keys=[assigned_to]
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="issue",
        cascade="all, delete-orphan"
    )