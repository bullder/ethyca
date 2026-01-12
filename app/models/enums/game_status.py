from enum import Enum

class GameStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WON_X = "WON_X"
    WON_O = "WON_O"
    DRAW = "DRAW"
