import abc
from typing import Dict
from chalice import Response


class BaseResponse(abc.ABC):
    def __init__(self, origin: str = "*"):
        self.headers: Dict[str, str] = {}
        self.origin = origin

    @abc.abstractmethod
    def to_response(self) -> Response:
        pass

    def headers_with_cors(self):
        headers = {
            "Access-Control-Allow-Origin": self.origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
        }
        headers.update(self.headers)
        return headers
