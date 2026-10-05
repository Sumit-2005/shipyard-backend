from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/projects",
    tags=['Projects']
)

@router.get("/", response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    projects = db.query(models.Project).filter(models.Project.user_id == current_user.id).filter(models.Project.overview.contains(search)).limit(limit).offset(skip).all()
    return projects

@router.get("/{id}", response_model=schemas.ProjectOut)
def get_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == id).filter(models.Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} does not exist")
    return project

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    new_project = models.Project(user_id=current_user.id, **project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    project = project_query.first()

    if project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} does not exist")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    project_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ProjectOut)
def update_project(id: int, updated_project: schemas.ProjectBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    project_query = db.query(models.Project).filter(models.Project.id == id)
    project = project_query.first()

    if project == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project with id: {id} does not exist")

    if project.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    project_query.update(updated_project.model_dump(), synchronize_session=False)
    db.commit()
    return project_query.first()