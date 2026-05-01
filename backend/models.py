from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    reviews = relationship("Review", back_populates="user")

class Album(Base):
    __tablename__ = "albums"
    lastfm_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    cover_url = Column(String)
    
    reviews = relationship("Review", back_populates="album")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lastfm_id = Column(String, ForeignKey("albums.lastfm_id"))
    rating = Column(Float)
    review_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="reviews")
    album = relationship("Album", back_populates="reviews")
