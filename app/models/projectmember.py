
from sqlalchemy import  ForeignKey,DateTime,func,PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from typing import TYPE_CHECKING

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project




class ProjectMember(Base):
    __tablename__ = "project_members"


    project_id :Mapped[int] = mapped_column(ForeignKey("projects.id"),
                                            nullable=False)
    user_id :Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         nullable=False)
    joined_at :Mapped[datetime] = mapped_column(DateTime,
                                                server_default=func.now(),
                                                nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('project_id', 'user_id'),
    )

       # Relationships

    project: Mapped["Project"] = relationship(
        back_populates="memberships"
    )

    user: Mapped["User"] = relationship(
        back_populates="project_memberships"
    )

    