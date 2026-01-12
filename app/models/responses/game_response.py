from chalice import Response
from http import HTTPStatus
from app.models.game import Game
from app.models.responses.base_response import BaseResponse


class GameResponse(BaseResponse):
    def __init__(self, game: Game, status_code: int = HTTPStatus.OK, origin: str = "*"):
        super().__init__(origin)
        self.game = game
        self.status_code = status_code

    def to_response(self) -> Response:
        return Response(
            status_code=self.status_code,
            body=self.game.model_dump(mode='json'),
            headers=self.headers_with_cors()
        )
