import json
import os.path

import uvicorn
from fastapi import FastAPI

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


@app.get("/api/layout/{game}")
def get_control_layout(game: str):
    layout_path = os.path.join(LAYOUTS_FOLDER_PATH, game.lower() + ".json")

    if not os.path.exists(layout_path):
        return error("Game not found")

    with open(layout_path) as handle:
        layout = json.loads(handle.read())
        return success(layout)


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    start_server()