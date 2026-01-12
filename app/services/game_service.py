from typing import Optional
from app.models import (
    Game,
    GameNotFoundError,
    GameMove,
)
from .game_repository import GameRepository

class GameService:
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def create_game(self) -> Game:
        game = Game()
        self.repository.save_game(game)
        return game

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.repository.get_game(game_id)

    def list_games(self, limit: int = 100) -> list[Game]:
        return self.repository.list_games(limit)

    def make_move(self, request: GameMove) -> Game:
        game = self.repository.get_game(request.game_id)
        if not game:
            raise GameNotFoundError(game_id=request.game_id)
        
        game.process_move(request.move)

        self.repository.save_game(game)
        return game
