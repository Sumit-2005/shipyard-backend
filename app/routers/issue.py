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
def get_issues(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    issues = db.query(models.Issue).filter(models.Issue.assignee == current_user.id).filter(models.Issue.label.contains(search)).limit(limit).offset(skip).all()
    return issues

@router.get("/{id}", response_model=schemas.IssueOut)
def get_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    issue = db.query(models.Issue).filter(models.Issue.id == id).filter(models.Issue.assignee == current_user.id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Issue with id: {id} does not exist")
    return issue

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.IssueOut)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_issue = models.Issue(assignee=current_user.id, **issue.model_dump())
    project = db.query(models.Project).filter(models.Project.id == issue.project_id).first()

    if not project: 
        raise HTTPException(status_code=404, 
                            detail="Project not found")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Not authorized for this Project")
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    issue_query = db.query(models.Issue).filter(models.Issue.id == id)
    issue = issue_query.first()

    if issue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Issue with id: {id} does not exist")

    if issue.assignee != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    issue_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.IssueOut)
def update_issue(id: int, updated_issue: schemas.IssueBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    issue_query = db.query(models.Issue).filter(models.Issue.id == id)
    issue = issue_query.first()

    if issue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Issue with id: {id} does not exist")

    if issue.assignee != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    issue_query.update(updated_issue.model_dump(), synchronize_session=False)
    db.commit()
    return issue_query.first()