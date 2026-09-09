from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.issue import Issue


def create_issue(
    db: Session,
    project_id: int,
    title: str,
    description: str | None,
    priority,
    created_by: int
):
    issue = Issue(
        project_id=project_id,
        title=title,
        description=description,
        priority=priority,
        created_by=created_by
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue

def get_issue_by_id(db: Session, issue_id: int):
    statement = select(Issue).where(Issue.id == issue_id)
    return db.scalars(statement).first()

def get_issues_by_project(
    db: Session,
    project_id: int,
    status_filter=None,
    priority_filter=None,
    offset: int = 0,
    limit: int = 20
):
    statement = select(Issue).where(
        Issue.project_id == project_id
    )

    if status_filter is not None:
        statement = statement.where(
            Issue.status == status_filter
        )

    if priority_filter is not None:
        statement = statement.where(
            Issue.priority == priority_filter
        )

    statement = (
        statement
        .offset(offset)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_issue(
    db: Session,
    issue: Issue,
    data: dict
):
    for field, value in data.items():
        setattr(issue, field, value)

    db.commit()
    db.refresh(issue)

    return issue



def delete_issue(
    db: Session,
    issue: Issue
):
    db.delete(issue)
    db.commit()


def assign_issue(
    db: Session,
    issue: Issue,
    user_id: int
):
    issue.assigned_to = user_id

    db.commit()
    db.refresh(issue)

    return issue