from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import requests
from typing import List
import os
from dotenv import load_dotenv

from . import models, schemas, auth
from .database import engine, get_db

# Load environment variables from .env file
load_dotenv()

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SleeveNotes API")

# You should define this in your environment or Render dashboard
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/reviews", response_model=schemas.ReviewResponse)
def log_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # 1. Check if album exists, if not create it
    album = db.query(models.Album).filter(models.Album.lastfm_id == review.album.lastfm_id).first()
    if not album:
        album = models.Album(
            lastfm_id=review.album.lastfm_id,
            title=review.album.title,
            artist=review.album.artist,
            cover_url=review.album.cover_url
        )
        db.add(album)
        db.commit()
        db.refresh(album)
    
    # 2. Create the review
    new_review = models.Review(
        user_id=current_user.id,
        lastfm_id=album.lastfm_id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get("/feed", response_model=List[schemas.FeedItem])
def get_feed(db: Session = Depends(get_db)):
    # Get the 50 most recent reviews
    reviews = db.query(models.Review).order_by(models.Review.created_at.desc()).limit(50).all()
    
    feed = []
    for r in reviews:
        feed.append(schemas.FeedItem(
            review_id=r.id,
            username=r.user.username,
            album_title=r.album.title,
            album_artist=r.album.artist,
            album_cover_url=r.album.cover_url,
            rating=r.rating,
            review_text=r.review_text,
            created_at=r.created_at
        ))
    return feed

@app.get("/search")
def search_lastfm(q: str):
    if not LASTFM_API_KEY:
        raise HTTPException(status_code=500, detail="Last.fm API key not configured on server")
        
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.search&album={q}&api_key={LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Last.fm API error")
        
    data = response.json()
    albums = data.get("results", {}).get("albummatches", {}).get("album", [])
    
    # Clean up results
    results = []
    for a in albums:
        # Last.fm returns an array of images. We want the largest one.
        images = a.get("image", [])
        cover_url = ""
        for img in images:
            if img.get("size") in ["extralarge", "mega"] and img.get("#text"):
                cover_url = img.get("#text")
                break
        if not cover_url and len(images) > 0:
            cover_url = images[-1].get("#text", "")
            
        # We use mbid as the primary key. If none exists, we generate a slug.
        lastfm_id = a.get("mbid")
        if not lastfm_id:
            lastfm_id = f"{a.get('artist')}-{a.get('name')}".replace(" ", "-").lower()
            
        results.append({
            "lastfm_id": lastfm_id,
            "title": a.get("name"),
            "artist": a.get("artist"),
            "cover_url": cover_url
        })
        
    return results

@app.get("/album/info")
def get_album_info(artist: str, album: str):
    import urllib.parse
    if not LASTFM_API_KEY:
        raise HTTPException(status_code=500, detail="Last.fm API key not configured")
        
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LASTFM_API_KEY}&artist={urllib.parse.quote(artist)}&album={urllib.parse.quote(album)}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Last.fm API error")
        
    data = response.json()
    album_data = data.get("album", {})
    if not album_data:
        return {"tracks": [], "tags": [], "wiki": "No information found."}
    
    # Extract tracks
    tracks = []
    tracks_data = album_data.get("tracks", {}).get("track", []) if album_data.get("tracks") else []
    if isinstance(tracks_data, dict): 
        tracks_data = [tracks_data]
    for t in tracks_data:
        duration_int = int(t.get("duration", 0)) if t.get("duration") else 0
        mins = duration_int // 60
        secs = duration_int % 60
        tracks.append({
            "name": t.get("name"),
            "duration": f"{mins}:{secs:02d}" if duration_int > 0 else ""
        })
        
    # Extract tags
    tags = []
    tags_data = album_data.get("tags", {}).get("tag", []) if album_data.get("tags") else []
    if isinstance(tags_data, dict):
        tags_data = [tags_data]
    for tag in tags_data:
        tags.append(tag.get("name"))
        
    wiki = album_data.get("wiki", {}).get("summary", "No description available.")
    
    return {
        "tracks": tracks,
        "tags": tags,
        "wiki": wiki
    }

@app.get("/profile")
def get_profile(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    reviews = db.query(models.Review).filter(models.Review.user_id == current_user.id).order_by(models.Review.created_at.desc()).all()
    
    results = []
    for r in reviews:
        results.append({
            "review_id": r.id,
            "album_title": r.album.title,
            "album_artist": r.album.artist,
            "album_cover_url": r.album.cover_url,
            "rating": r.rating,
            "review_text": r.review_text,
            "created_at": r.created_at
        })
    return {"username": current_user.username, "reviews": results}
