from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AlbumBase(BaseModel):
    lastfm_id: str
    title: str
    artist: str
    cover_url: str

class ReviewCreate(BaseModel):
    album: AlbumBase
    rating: float
    review_text: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    lastfm_id: str
    rating: float
    review_text: str
    created_at: datetime
    class Config:
        orm_mode = True

class FeedItem(BaseModel):
    review_id: int
    username: str
    album_title: str
    album_artist: str
    album_cover_url: str
    rating: float
    review_text: str
    created_at: datetime
