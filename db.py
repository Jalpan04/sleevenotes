import sqlite3
from datetime import datetime
import os

DB_NAME = "sleevenotes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        bio TEXT
    )''')
    
    # Albums Table
    c.execute('''CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        year INTEGER,
        color TEXT
    )''')
    
    # Reviews/Diary Table
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        album_id INTEGER,
        rating REAL,
        review_text TEXT,
        liked BOOLEAN,
        date_logged TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(album_id) REFERENCES albums(id)
    )''')
    
    # Insert Dummy User
    c.execute("SELECT count(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, bio) VALUES ('Jax', 'Chronically ironic')")
        
    # Insert Dummy Albums
    c.execute("SELECT count(*) FROM albums")
    if c.fetchone()[0] == 0:
        dummy_albums = [
            ("Echoes of Silence", "The Weeknd", 2011, "0.55,0.1,0.1"),
            ("Random Access Memories", "Daft Punk", 2013, "0.15,0.15,0.35"),
            ("Blonde", "Frank Ocean", 2016, "0.9,0.55,0.2"),
            ("In Rainbows", "Radiohead", 2007, "0.75,0.2,0.15"),
            ("Abbey Road", "The Beatles", 1969, "0.2,0.5,0.7"),
            ("Rumours", "Fleetwood Mac", 1977, "0.3,0.2,0.15"),
        ]
        c.executemany("INSERT INTO albums (title, artist, year, color) VALUES (?, ?, ?, ?)", dummy_albums)
        
    conn.commit()
    conn.close()

def get_albums():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, artist, year, color FROM albums")
    albums = c.fetchall()
    conn.close()
    return [{"id": a[0], "title": a[1], "artist": a[2], "year": a[3], "color": tuple(map(float, a[4].split(',')))} for a in albums]

def log_review(user_id, album_id, rating, review_text, liked):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date_str = datetime.now().strftime("%B %d, %Y")
    c.execute("""
        INSERT INTO reviews (user_id, album_id, rating, review_text, liked, date_logged)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, album_id, rating, review_text, liked, date_str))
    conn.commit()
    conn.close()

def get_diary(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT a.title, r.rating, r.date_logged, r.review_text
        FROM reviews r
        JOIN albums a ON r.album_id = a.id
        WHERE r.user_id = ?
        ORDER BY r.id DESC
    """, (user_id,))
    reviews = c.fetchall()
    conn.close()
    return [{"title": r[0], "rating": r[1], "date": r[2], "review": r[3]} for r in reviews]

# Initialize on import
init_db()
