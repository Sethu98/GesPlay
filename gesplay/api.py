import os.path

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from gesplay.constants import LAYOUTS_FOLDER_PATH
from gesplay.gesture_handler import GestureHandler
from gesplay.util import Utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AppState:
    def __init__(self):
        self.current_game = None
        self.gesture_handler = GestureHandler({})


app_state = AppState()


def success(resp):
    return {
        'success': True,
        'data': resp
    }


def error(resp):
    return {
        'success': False,
        'error': resp
    }


class UpdateControlsRequest(BaseModel):
    game: str
    gesture: str
    new_key: str


@app.get("/api/games-list")
def get_games():
    return success([file.split('.')[0] for file in os.listdir(LAYOUTS_FOLDER_PATH)])


# @app.get("/api/keyboard-keys")
# def get_keyboard_keys():
#     return success(pyautogui.KEYBOARD_KEYS)


@app.post("/api/update-controls")
def update_controls(request: UpdateControlsRequest):
    print("Current game: ", app_state.current_game)

    try:
        layout = Utils.read_layout(request.game)
        if layout is None:
            return error("Game not found")

        if request.new_key == 'Unmapped':
            layout.pop(request.gesture)
        else:
            layout[request.gesture] = request.new_key

        Utils.write_layout(request.game, layout)

        print(f"Updated controls for request: {request}")

        if request.game == app_state.current_game:
            app_state.gesture_handler.set_gesture_to_key_map(layout)

        return success(layout)
    except Exception as e:
        print(f"Error while updating controls: {e}")
        return error("Failed to update")


@app.post("/api/add-game")
def add_game(request: dict):
    try:
        game = request['game']
        layout_path = Utils.get_layout_file_path(game)
        if os.path.exists(layout_path):
            return error("Already exists")

        Utils.write_layout(game, {}, create_if_not_exists=True)  # Just write empty layout

        return success("Created")
    except:
        return error("Failed to add")


@app.post("/api/remove-game")
def remove_game(request: dict):
    try:
        game = request['game']
        layout_path = Utils.get_layout_file_path(game)
        if not os.path.exists(layout_path):
            return error("Does not exist")

        os.remove(layout_path)
        print(f"Removed game: {game}")

        return success("Deleted")
    except Exception as e:
        print(f"Error while removing game: {e}")
        return error("Failed to add")


@app.get("/api/layout/{game}")
def get_control_layout(game: str):
    try:
        layout = Utils.read_layout(game)

        if layout is None:
            return error("Game not found")

        return success(layout)
    except Exception as e:
        print(f"Error while fetching controls: {e}")
        return error("Failed to fetch controls")


@app.post("/api/set-current-game")
def set_current_game(request: dict):
    game = request['game']
    app_state.current_game = game
    layout = Utils.read_layout(game)

    if layout:
        app_state.gesture_handler.set_gesture_to_key_map(layout)


def start_http_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)

# if __name__ == "__main__":
#     start_http_server()
