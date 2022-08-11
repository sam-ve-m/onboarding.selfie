# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.exceptions import (
    ErrorOnSendAuditLog,
    ErrorOnDecodeJwt,
    SelfieNotExists,
    OnboardingStepsStatusCodeNotOk,
    InvalidOnboardingCurrentStep,
    ErrorOnGetUniqueId,
)
from src.domain.response.model import ResponseModel
from src.domain.validator import Base64
from src.services.jwt import JwtService
from src.services.selfie import SelfieService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


async def selfie() -> Response:
    raw_selfie = request.json
    jwt = request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        selfie_validated = Base64(**raw_selfie).dict()
        await SelfieService.validate_current_onboarding_step(jwt=jwt)
        success = await SelfieService.save_user_selfie(
            selfie_validated=selfie_validated, unique_id=unique_id
        )
        response = ResponseModel(
            success=success,
            message="User selfie saved successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="Current step is not user selfie",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except SelfieNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.info(ex=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid, extra or missing params",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
