# SleeveNotes - Sample Data
# Album cover colors (solid placeholders)

ALBUMS = [
    {"id": 1, "title": "Echoes of Silence", "artist": "The Weeknd", "year": 2011, "genre": "R&B", "color": (0.55, 0.1, 0.1), "rating": 4.5},
    {"id": 2, "title": "Random Access Memories", "artist": "Daft Punk", "year": 2013, "genre": "Electronic", "color": (0.15, 0.15, 0.35), "rating": 4.8},
    {"id": 3, "title": "Blonde", "artist": "Frank Ocean", "year": 2016, "genre": "R&B", "color": (0.9, 0.55, 0.2), "rating": 4.7},
    {"id": 4, "title": "In Rainbows", "artist": "Radiohead", "year": 2007, "genre": "Alt Rock", "color": (0.75, 0.2, 0.15), "rating": 4.6},
    {"id": 5, "title": "Abbey Road", "artist": "The Beatles", "year": 1969, "genre": "Rock", "color": (0.2, 0.5, 0.7), "rating": 4.9},
    {"id": 6, "title": "Rumours", "artist": "Fleetwood Mac", "year": 1977, "genre": "Rock", "color": (0.3, 0.2, 0.15), "rating": 4.7},
    {"id": 7, "title": "Thriller", "artist": "Michael Jackson", "year": 1982, "genre": "Pop", "color": (0.7, 0.6, 0.1), "rating": 4.8},
    {"id": 8, "title": "Back to Black", "artist": "Amy Winehouse", "year": 2006, "genre": "Soul", "color": (0.12, 0.12, 0.12), "rating": 4.5},
    {"id": 9, "title": "Currents", "artist": "Tame Impala", "year": 2015, "genre": "Psychedelic", "color": (0.6, 0.15, 0.4), "rating": 4.4},
    {"id": 10, "title": "Channel Orange", "artist": "Frank Ocean", "year": 2012, "genre": "R&B", "color": (0.9, 0.5, 0.05), "rating": 4.6},
    {"id": 11, "title": "OK Computer", "artist": "Radiohead", "year": 1997, "genre": "Alt Rock", "color": (0.3, 0.3, 0.35), "rating": 4.7},
    {"id": 12, "title": "Dark Side of the Moon", "artist": "Pink Floyd", "year": 1973, "genre": "Prog Rock", "color": (0.05, 0.05, 0.2), "rating": 4.9},
    {"id": 13, "title": "Nevermind", "artist": "Nirvana", "year": 1991, "genre": "Grunge", "color": (0.1, 0.4, 0.6), "rating": 4.5},
    {"id": 14, "title": "The Miseducation", "artist": "Lauryn Hill", "year": 1998, "genre": "Hip-Hop", "color": (0.5, 0.35, 0.15), "rating": 4.8},
    {"id": 15, "title": "Kid A", "artist": "Radiohead", "year": 2000, "genre": "Electronic", "color": (0.6, 0.65, 0.7), "rating": 4.5},
    {"id": 16, "title": "Lemonade", "artist": "Beyonce", "year": 2016, "genre": "Pop", "color": (0.85, 0.75, 0.1), "rating": 4.6},
]

DIARY_ENTRIES = [
    {"day": 1, "month": "MAY 2026", "album": ALBUMS[0], "rating": 4.5, "relisten": False, "has_review": True},
    {"day": 29, "month": "APRIL 2026", "album": ALBUMS[1], "rating": 5.0, "relisten": True, "has_review": True},
    {"day": 26, "month": "APRIL 2026", "album": ALBUMS[2], "rating": 4.0, "relisten": False, "has_review": False},
    {"day": 25, "month": "APRIL 2026", "album": ALBUMS[3], "rating": 4.0, "relisten": False, "has_review": True},
    {"day": 24, "month": "APRIL 2026", "album": ALBUMS[4], "rating": 5.0, "relisten": False, "has_review": False},
    {"day": 23, "month": "APRIL 2026", "album": ALBUMS[5], "rating": 3.0, "relisten": True, "has_review": True},
    {"day": 23, "month": "APRIL 2026", "album": ALBUMS[6], "rating": 4.5, "relisten": False, "has_review": False},
    {"day": 19, "month": "APRIL 2026", "album": ALBUMS[7], "rating": 4.0, "relisten": False, "has_review": True},
    {"day": 17, "month": "APRIL 2026", "album": ALBUMS[8], "rating": 5.0, "relisten": False, "has_review": False},
    {"day": 11, "month": "APRIL 2026", "album": ALBUMS[9], "rating": 3.0, "relisten": False, "has_review": False},
    {"day": 7, "month": "APRIL 2026", "album": ALBUMS[10], "rating": 3.5, "relisten": True, "has_review": True},
]

ACTIVITY_ITEMS = [
    {"type": "listenlist_add", "user": "You", "album": "Echoes of Silence", "time": "20h", "avatar_color": (0.3, 0.5, 0.3)},
    {"type": "rated", "user": "Dev!", "album": "Random Access Memories", "time": "1d", "rating": 4.5, "date_str": "Thursday, May 1, 2026", "avatar_color": (0.4, 0.3, 0.5)},
    {"type": "listened", "user": "You", "album": "Blonde", "time": "2d", "rating": 4.5, "review": "Peak", "album_color": (0.9, 0.55, 0.2), "avatar_color": (0.3, 0.5, 0.3)},
    {"type": "liked_review", "user": "You", "target_user": "musichead42", "album": "In Rainbows", "time": "5d", "rating": 3.0, "avatar_color": (0.3, 0.5, 0.3)},
    {"type": "listenlist_add", "user": "You", "album": "Currents", "time": "5d", "avatar_color": (0.3, 0.5, 0.3)},
    {"type": "listenlist_add", "user": "You", "album": "Kid A", "time": "5d", "avatar_color": (0.3, 0.5, 0.3)},
    {"type": "listened", "user": "You", "album": "Abbey Road", "time": "5d", "rating": 3.0, "review": "timeless masterpiece", "album_color": (0.2, 0.5, 0.7), "avatar_color": (0.3, 0.5, 0.3)},
]

CATEGORIES = [
    "Release Date", "Genre & Style", "Highest Rated",
    "Most Anticipated", "Top 500 Studio Albums", "Decades",
]
