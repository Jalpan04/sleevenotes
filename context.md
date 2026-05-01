# Project Context: SleeveNotes

## Overview
SleeveNotes is a social music-logging application where users can search for albums, write reviews, and see a live feed of what their friends are listening to.

## Tech Stack
- **Mobile App**: Kivy & KivyMD (Python)
- **Backend API**: FastAPI
- **Database**: SQLAlchemy with SQLite (Dev) / PostgreSQL (Production via Neon/Supabase)
- **External Data**: Last.fm API
- **Deployment**: Buildozer (Android APK), Render/Railway (Cloud Hosting)

## Current Status (Phase 2 Completed)
1. **MVP Build**: Successfully compiled a local-only APK that runs on Android devices.
2. **Backend Foundation**: FastAPI server implemented with User, Album, and Review models.
3. **Authentication**: JWT-based login and signup system is functional.
4. **Data Bridge**: Server-side search proxy for Last.fm is ready.
5. **Git History**: Repository initialized with a clean, incremental commit history on GitHub.

## Next Steps
- **Phase 3**: Refactor the Kivy frontend to remove local SQLite logic and integrate the FastAPI networking layer.
- **Phase 4**: Cloud deployment of the FastAPI backend.
- **Phase 5**: Final production APK build with social feed integration.

## Key Files
- `main.py`: Current Kivy frontend (needs refactoring).
- `backend/main.py`: FastAPI entry point.
- `buildozer.spec`: Android packaging configuration.
- `bin/`: Stores the latest compiled APK.
