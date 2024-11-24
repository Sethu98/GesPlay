import enum


class Hand(enum.Enum):
    LEFT = 'left'
    RIGHT = 'right'


class Gestures(enum.Enum):
    INDEX_OUT = 'index_out'
    THUMB_OUT = 'thumb_out'
    PINKY_OUT = 'pinky_out'