import os.path
import sys
import threading

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from gesplay.gp import GesPlay

from gesplay.api import start_http_server, app_state

if __name__ == "__main__":
    t = threading.Thread(target=start_http_server)
    t.start()
    GesPlay(app_state.gesture_handler).start()
    t.join()
