from datetime import datetime
from sqlalchemy import  Integer, String, ForeignKey,func,DateTime,Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import TYPE_CHECKING
from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.projectmember import ProjectMember
    from app.models.issue import Issue

class Project(Base):
    __tablename__ = "projects"

    id :Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    index=True)
    name :Mapped[str] = mapped_column(String(100),
                                       nullable=False)
    description :Mapped[str | None] = mapped_column(Text,
                                             nullable=True)
    created_by :Mapped[int] = mapped_column(ForeignKey("users.id"),
                                          nullable=False)
    created_at :Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now(),
                                                 nullable=False)
    updated_at :Mapped[datetime] = mapped_column(DateTime,
                                                 server_default=func.now(),
                                                    onupdate=func.now(),
                                                    nullable=False)

    # Relationships
    creator: Mapped["User"] = relationship(
        back_populates="created_projects"
    )

    memberships: Mapped[list["ProjectMember"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    issues: Mapped[list["Issue"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    