from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from app import oauth2
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get("/me", response_model=schemas.UserOut)
def get_user(current_user: int = Depends(oauth2.get_current_user)):
    return current_user