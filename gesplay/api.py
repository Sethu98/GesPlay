import json
import os.path

import pyautogui
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from gesplay.constants import LAYOUTS_FOLDER_PATH
from gesplay.util import Utils

app = FastAPI()


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


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    start_server()
