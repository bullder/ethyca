from chalice import Response
from http import HTTPStatus
from app.models.game import Game
from app.models.responses.base_response import BaseResponse


class GameResponse(BaseResponse):
    def to_response(self, game: Game, status_code: int = HTTPStatus.OK) -> Response:
        return Response(
            status_code=status_code,
            body=game.model_dump(mode='json'),
            headers=self.headers_with_cors()
        )
