from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    overview: str
    deployment: str

class ProjectOut_Issues(ProjectBase):
    id: int

class ProjectOut(ProjectBase):
    id: int

    owner: UserOut


class ProjectCreate(ProjectBase):
    pass

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]

class IssueBase(BaseModel):
    label: str
    priority: int
    status: str

class IssueOut(IssueBase):
    id: int
    owner: UserOut
    project: ProjectOut_Issues

class IssueCreate(IssueBase):
    project_id: int