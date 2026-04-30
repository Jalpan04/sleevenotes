# SleeveNotes

SleeveNotes is a music-logging application built with Python and KivyMD, allowing users to log, rate, and review their favorite music albums locally. It serves as a personal diary for music enthusiasts.

## Features

- **Personal Diary**: Log reviews, ratings (out of 5 stars), and favorites for music albums.
- **Local Database**: All user data is stored securely offline using a persistent SQLite database.
- **Modern Interface**: Designed using KivyMD with a dark theme and mustard highlights for a sleek user experience.
- **Cross-Platform**: Built natively in Python, allowing packaging for Android via Buildozer.

## Installation and Usage

To run the application locally on a desktop environment:

1. Install the required dependencies:
   `pip install kivy kivymd`
2. Run the main application:
   `python main.py`

## Android Deployment

A pre-compiled Android Package Kit (APK) is provided in the `bin/` directory. 

To build the APK from source using Buildozer (Linux or Google Colab recommended):
1. Install dependencies:
   `pip install buildozer cython==0.29.33`
2. Execute the Buildozer debug build:
   `buildozer -v android debug`

## Project Structure

- `main.py`: Contains the core application logic and KivyMD frontend layout.
- `db.py`: Handles all SQLite database creation and queries.
- `data.py`: Provides data models or mock structures.
- `buildozer.spec`: Configuration file required for Android packaging.
- `bin/`: Contains the compiled Android APK installer.
