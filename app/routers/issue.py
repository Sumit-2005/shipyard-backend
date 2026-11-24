from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from app.routers import project

from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/issues",
    tags=['Issues']
)



@router.get("/", response_model=List[schemas.IssueOut])
def get_issues(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    project_id: Optional[int] = None
):
    issues = (
        db.query(models.Issue)
        .join(models.Project)
        .filter(models.Project.user_id == current_user.id)
        .filter(models.Issue.label.contains(search))
    )

    if project_id is not None:
        issues = issues.filter(models.Issue.project_id == project_id)

    issues = issues.limit(limit).offset(skip).all()

    return issues


@router.get("/{id}", response_model=schemas.IssueOut)
def get_issue(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    issue = (
        db.query(models.Issue)
        .join(models.Project)
        .filter(models.Issue.id == id)
        .filter(models.Project.user_id == current_user.id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id: {id} does not exist"
        )

    return issue



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.IssueOut
)
def create_issue(
    issue: schemas.IssueCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == issue.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this project"
        )

    new_issue = models.Issue(
        **issue.model_dump(),
        assignee=current_user.id
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    issue = (
        db.query(models.Issue)
        .join(models.Project)
        .filter(models.Issue.id == id)
        .filter(models.Project.user_id == current_user.id)
        .first()
    )

    if issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id: {id} does not exist"
        )

    db.delete(issue)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.IssueOut)
def update_issue(
    id: int,
    updated_issue: schemas.IssueBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    issue = (
        db.query(models.Issue)
        .join(models.Project)
        .filter(models.Issue.id == id)
        .filter(models.Project.user_id == current_user.id)
        .first()
    )

    if issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with id: {id} does not exist"
        )

    for key, value in updated_issue.model_dump().items():
        setattr(issue, key, value)

    db.commit()
    db.refresh(issue)

    return issue
