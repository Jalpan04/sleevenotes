# Development Rules for SleeveNotes

All code and contributions must strictly adhere to these guidelines.

## General Rules
- **No Emojis**: Never use emojis in commit messages, documentation, or code comments.
- **Conciseness**: Keep logic lean and avoid unnecessary dependencies.
- **Naming**: Use snake_case for Python files and variables.

## Frontend (Kivy/KivyMD)
- **Asynchronous Operations**: All network calls (to FastAPI or Last.fm) MUST be non-blocking. Use Kivy's `UrlRequest` or threading to prevent UI freezing.
- **Mobile-First Design**: Use `dp()` (density-independent pixels) for all sizing to ensure compatibility across different Android screen densities.
- **Theme**: Maintain the "Dark" theme with mustard (`#FFD700`) highlights.

## Backend (FastAPI)
- **Pydantic V2**: Always use Pydantic V2 syntax (e.g., `from_attributes = True` instead of `orm_mode = True`).
- **Security**: Never hardcode secrets. Use environment variables for `LASTFM_API_KEY`, `SECRET_KEY`, and `DATABASE_URL`.
- **Statelessness**: The API must remain stateless, using JWT tokens for authentication.

## Git & Deployment
- **Commits**: Use descriptive, professional commit messages.
- **Buildozer**: Maintain the `buildozer.spec` requirements list meticulously. Any new Python library must be added to the `requirements` line.
- **Versioning**: Follow semantic versioning for the APK releases.
