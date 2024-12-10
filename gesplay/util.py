import json
import os
from datetime import datetime as dt

from gesplay.constants import LAYOUTS_FOLDER_PATH


class Utils:
    @staticmethod
    def get_unix_timestamp_ms():
        return int(dt.now().timestamp() * 1000)

    @staticmethod
    def get_layout_file_path(game):
        return os.path.join(LAYOUTS_FOLDER_PATH, game.lower() + ".json")

    @staticmethod
    def read_layout(game):
        layout_path = Utils.get_layout_file_path(game)
        if not os.path.exists(layout_path):
            return None

        with open(layout_path) as handle:
            layout = json.loads(handle.read())
            return layout

    @staticmethod
    def write_layout(game, layout, create_if_not_exists=False):
        layout_path = Utils.get_layout_file_path(game)
        if not os.path.exists(layout_path) and not create_if_not_exists:
            return

        with open(layout_path, 'w') as handle:
            handle.write(json.dumps(layout, indent=4))
