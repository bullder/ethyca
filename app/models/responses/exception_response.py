from chalice import Response

from app.models import TicTacToeError
from app.models.responses.base_response import BaseResponse


class ExceptionResponse(BaseResponse):
    def __init__(self, err: TicTacToeError, origin: str = "*"):
        super().__init__(origin)
        self.err = err

    def to_response(self) -> Response:
        return Response(
            status_code=self.err.status_code,
            body={"detail": str(self.err.message)},
            headers=self.headers_with_cors()
        )
