from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.project import Project
from app.models.projectmember import ProjectMember

def create_project(
        db: Session,
        name: str,
        description: str | None,
        created_by: int
    ):
    #  CORRECT: Passing values by name (keyword arguments)
    project = Project(name=name, description=description, created_by=created_by)

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project_by_id(
    db: Session,
    project_id: int
):
    statement = select(Project).where(Project.id == project_id)

    return db.scalars(statement).first()


def get_projects(
    db: Session,
    offset: int,
    limit: int
):
    statement = (
        select(Project)
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


def get_project_member(
    db: Session,
    project_id: int,
    user_id: int
):
    statement = select(ProjectMember).where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    )

    return db.scalars(statement).first()

def add_project_member(
    db: Session,
    project_id: int,
    user_id: int
):
    membership = ProjectMember(
        project_id=project_id,
        user_id=user_id
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return membership

def get_project_members(
    db: Session,
    project_id: int
):
    statement = select(ProjectMember).where(
        ProjectMember.project_id == project_id
    )

    return db.scalars(statement).all()


def delete_project_member(
    db: Session,
    membership: ProjectMember
):
    db.delete(membership)
    db.commit()