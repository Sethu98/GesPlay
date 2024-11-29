from datetime import datetime as dt


class Utils:
    @staticmethod
    def get_unix_timestamp_ms():
        return int(dt.now().timestamp() * 1000)
