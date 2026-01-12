from pydantic import BaseModel
from app.models.requests.move import Move

class GameMove(BaseModel):
    game_id: str
    move: Move
