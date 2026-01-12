from http import HTTPStatus
from typing import Any

class TicTacToeError(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    
    def __init__(self, message: str, **context: Any):
        super().__init__(message)
        self.message = message
        self.context = context

class GameNotFoundError(TicTacToeError):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, game_id: str):
        super().__init__(f"Game not found: {game_id}", game_id=game_id)

class GameFinishedError(TicTacToeError):
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(self, game_id: str):
        super().__init__("Game is already finished", game_id=game_id)

class InvalidTurnError(TicTacToeError):
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(self, game_id: str, expected: str, actual: str):
        super().__init__(
            f"It is not {actual}'s turn", 
            game_id=game_id, 
            expected_turn=expected, 
            actual_turn=actual
        )

class InvalidMoveError(TicTacToeError):
    status_code = HTTPStatus.BAD_REQUEST

class InvalidPositionError(InvalidMoveError):
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(self, game_id: str, x: int, y: int):
        super().__init__(f"Invalid coordinates: ({x}, {y})", game_id=game_id, x=x, y=y)

class PositionOccupiedError(InvalidMoveError):
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(self, game_id: str, x: int, y: int):
        super().__init__("Position already occupied", game_id=game_id, x=x, y=y)

class BadRequestError(TicTacToeError):
    status_code = HTTPStatus.BAD_REQUEST

class NotFoundError(TicTacToeError):
    status_code = HTTPStatus.NOT_FOUND

class InternalServerError(TicTacToeError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
