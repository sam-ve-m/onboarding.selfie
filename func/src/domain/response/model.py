# Jormungandr - Onboarding
from ...domain.enums.code import InternalCode

# Standards
from json import dumps

# Third party
from flask import Response


class ResponseModel:
    def __init__(
        self, success: bool, code: InternalCode, message: str = None
    ):
        self.success = success
        self.code = code
        self.message = message
        self.response = self.to_dumps()

    def to_dumps(self) -> str:
        response_model = dumps(
            {
                "message": self.message,
                "success": self.success,
                "code": self.code,
            }
        )
        self.response = response_model
        return response_model

    def build_http_response(
        self, status: int, mimetype: str = "application/json"
    ) -> Response:
        http_response = Response(
            self.response,
            mimetype=mimetype,
            status=status,
        )
        return http_response
