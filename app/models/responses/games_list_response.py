from chalice import Response
from http import HTTPStatus
from app.models.game import Game
from app.models.responses.base_response import BaseResponse


class GamesListResponse(BaseResponse):
    def to_response(self, games: list[Game]) -> Response:
        return Response(
            status_code=HTTPStatus.OK,
            body=[game.to_list_item() for game in games],
            headers=self.headers_with_cors()
        )
