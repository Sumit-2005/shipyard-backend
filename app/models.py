from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, ForeignKey
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
