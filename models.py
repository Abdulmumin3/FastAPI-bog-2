from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=False, default=func.now())
    
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    
    # Additional methods to format datetime values

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)    
    password = Column(String)

    posts = relationship("Post", back_populates="author")
