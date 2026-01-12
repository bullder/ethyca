from chalice import Response
from http import HTTPStatus
from app.models.game import Game
from app.models.responses.base_response import BaseResponse


class GamesListResponse(BaseResponse):
    def __init__(self, games: list[Game], origin: str = "*"):
        super().__init__(origin)
        self.games = games

    def to_response(self) -> Response:
        return Response(
            status_code=HTTPStatus.OK,
            body=[game.to_list_item() for game in self.games],
            headers=self.headers_with_cors()
        )
