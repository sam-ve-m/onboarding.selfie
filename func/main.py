# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.exceptions import ErrorOnSendAuditLog, ErrorOnDecodeJwt
from src.domain.response.model import ResponseModel
from src.domain.validator import FileBase64
from src.services.jwt import JwtService
from src.services.service import SelfieService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


async def selfie():
    raw_selfie = request.json
    jwt = request.headers.get("x-thebes-answer")
    unique_id = JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    msg_error = "Unexpected error occurred"
    try:
        selfie_validated = FileBase64(**raw_selfie).dict()
        success = await SelfieService.save_user_selfie(selfie_validated=selfie_validated, unique_id=unique_id)
        response = ResponseModel(
            success=success,
            message="User selfie saved successfully",
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

if __name__ == '__main__':
    import asyncio

    response = asyncio.run()