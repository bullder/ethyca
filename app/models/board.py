import random
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from app.models.requests.move import Move
from app.models.enums.player import Player

class Board(BaseModel):
    cells: List[Optional[Player]] = Field(default_factory=lambda: [None] * 9)

    def __getitem__(self, index: int) -> Optional[Player]:
        return self.cells[index]

    def __setitem__(self, index: int, value: Player):
        self.cells[index] = value

    def is_full(self) -> bool:
        return all(cell is not None for cell in self.cells)

    def is_occupied(self, index: int) -> bool:
        return self.cells[index] is not None
    
    def check_winner(self) -> Optional[Player]:
        winning_combinations: List[Tuple[int, int, int]] = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in winning_combinations:
            if self._check_combination(combo):
                return self.cells[combo[0]]
        return None

    def get_random_available_cell(self) -> Optional[Move]:
        available_moves = [i for i, cell in enumerate(self.cells) if cell is None]
        if not available_moves:
            return None
        return Move.from_index(random.choice(available_moves))

    def _check_combination(self, combo: Tuple[int, int, int]) -> bool:
        a, b, c = combo
        return (
            self.cells[a] is not None
            and self.cells[a] == self.cells[b]
            and self.cells[a] == self.cells[c]
        )
