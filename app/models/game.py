from typing import Optional, List
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_serializer, field_validator

from app.models.enums.player import Player
from app.models.enums.game_status import GameStatus
from app.models.requests.move import Move
from .board import Board
from .exceptions import (
    GameFinishedError,
    InvalidTurnError,
    InvalidPositionError,
    PositionOccupiedError
)

class Game(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    board: Board = Field(default_factory=Board)
    current_turn: Player = Player.X
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[Player] = None
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    history: List[Move] = Field(default_factory=list)

    @field_serializer('board')
    def serialize_board(self, board: Board, _info):
        return board.cells

    @field_validator('board', mode='before')
    @classmethod
    def validate_board(cls, v):
        if isinstance(v, list):
            return Board(cells=v)
        return v

    def to_list_item(self) -> dict[str, str]:
        return {
            "id": self.id,
            "status": self.status.value,
            "started_at": self.started_at
        }

    def _update(self):
        winner = self.board.check_winner()
        if winner:
            self.status = GameStatus.WON_X if winner == Player.X else GameStatus.WON_O
            self.winner = winner
        elif self.board.is_full():
            self.status = GameStatus.DRAW
            self.winner = None
        else:
             pass

    def _make_computer_move(self):
        move = self.board.get_random_available_cell()
        if not move:
            return
        self.board.cells[move.position] = Player.O
        self.history.append(move)
        self.current_turn = Player.X
        self._update()

    def _validate_move(self, move: Move, player: Player):
        if self.status != GameStatus.IN_PROGRESS:
            raise GameFinishedError(game_id=self.id)

        if self.current_turn != player:
            raise InvalidTurnError(game_id=self.id, expected=self.current_turn.value, actual=player.value)

        if not (0 <= move.position <= 8):
             raise InvalidPositionError(game_id=self.id, x=move.x, y=move.y) 

        if self.board.is_occupied(move.position):
            raise PositionOccupiedError(game_id=self.id, x=move.x, y=move.y)

    def process_move(self, move: Move, player: Player = Player.X):
        self._validate_move(move, player)
        self.board.cells[move.position] = player
        self.history.append(move)
        
        self._update()
        
        if self.status == GameStatus.IN_PROGRESS:
            self.current_turn = self.get_next_player()
            if self.is_computer_turn():
                self._make_computer_move()

    def get_next_player(self) -> Player:
        return Player.O if self.current_turn == Player.X else Player.X

    def is_computer_turn(self) -> bool:
        return self.current_turn == Player.O