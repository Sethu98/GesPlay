import json
import os.path

import pyautogui
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from gesplay.constants import LAYOUTS_FOLDER_PATH

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


def read_layout(game):
    layout_path = os.path.join(LAYOUTS_FOLDER_PATH, game.lower() + ".json")

    if not os.path.exists(layout_path):
        return None

    with open(layout_path) as handle:
        layout = json.loads(handle.read())
        return layout


def write_layout(game, layout):
    layout_path = os.path.join(LAYOUTS_FOLDER_PATH, game.lower() + ".json")
    if not os.path.exists(layout_path):
        return

    with open(layout_path, 'w') as handle:
        handle.write(json.dumps(layout, indent=4))


@app.get("/api/games-list")
def get_games():
    return success([file.split('.')[0] for file in os.listdir(LAYOUTS_FOLDER_PATH)])


@app.get("/api/keyboard-keys")
def get_keyboard_keys():
    return success(pyautogui.KEYBOARD_KEYS)


@app.post("/api/update-controls/")
def update_controls(request: UpdateControlsRequest):
    try:
        layout = read_layout(request.game)
        if layout is None:
            return error("Game not found")

        layout[request.gesture] = layout[request.new_key]
        write_layout(request.game, layout)

        return success(layout)
    except:
        return error("Failed to update")


@app.get("/api/layout/{game}")
def get_control_layout(game: str):
    try:
        layout = read_layout(game)

        if layout is None:
            return error("Game not found")

        return success(layout)
    except:
        return error("Failed to fetch controls")


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    start_server()
