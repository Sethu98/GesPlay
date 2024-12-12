import enum


class Hand(enum.Enum):
    LEFT = 'left'
    RIGHT = 'right'


class Gestures(enum.Enum):
    CLOSED_FIST = 'Closed_Fist'
    OPEN_PALM = 'Open_Palm'
    POINTING_UP = 'Pointing_Up'
    THUMB_UP = 'Thumb_Up'
    THUMB_DOWN = 'Thumb_Down'
    VICTORY = 'Victory'
    UNKNOWN = 'Unknown'
    ILOVEYOU = 'ILoveYou'


LAYOUTS_FOLDER_PATH = 'layouts'
