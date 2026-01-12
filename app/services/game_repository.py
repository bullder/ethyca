from abc import ABC, abstractmethod
from typing import Optional
from app.models import Game

class GameRepository(ABC):
    @abstractmethod
    def save_game(self, game: Game) -> Game:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Optional[Game]:
        pass

    @abstractmethod
    def list_games(self, limit: int = 100) -> list[Game]:
        pass
