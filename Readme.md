# Gesplay

Gesplay is a hand gesture based video game controller that can be used to play any game with simple control layouts. It's built in Python and uses OpenCV, Google Mediapipe's hand tracking libraries and Pyautogui.

## Running the frontend

### Install flutter
Follow [this](https://docs.flutter.dev/get-started/install) to install flutter.

### Run
```bash
cd gesplay_gui
flutter run -d chrome
```

## Running the backend
```bash
# Create virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate # If you're using Linux/MacOS
.venv\Scripts\activate.bat # If you're using Windows

# Install dependencies
python3 -m pip install -r requirements.txt

# Run
python3 gp_main.py
```