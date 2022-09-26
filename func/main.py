# Jormungandr - Onboarding
from src.domain.enums.code import InternalCode
from src.domain.exceptions.exceptions import (
    ErrorOnSendAuditLog,
    ErrorOnDecodeJwt,
    SelfieNotExists,
    OnboardingStepsStatusCodeNotOk,
    InvalidOnboardingCurrentStep,
    ErrorOnGetUniqueId,
    ErrorSendingToIaraValidateSelfie,
)
from src.domain.response.model import ResponseModel
from src.domain.validators.validator import Base64File
from src.services.jwt import JwtService
from src.services.selfie import SelfieService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
import flask


async def selfie() -> flask.Response:
    raw_selfie = flask.request.json
    jwt = flask.request.headers.get("x-thebes-answer")
    msg_error = "Unexpected error occurred"
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        selfie_validated = Base64File(**raw_selfie)
        await SelfieService.validate_current_onboarding_step(jwt=jwt)
        success = await SelfieService.save_user_selfie(
            selfie_validated=selfie_validated, unique_id=unique_id
        )
        response = ResponseModel(
            success=success,
            message="User selfie saved successfully",
            code=InternalCode.SUCCESS.value,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID.value, message="Unauthorized token"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE.value,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT.value,
            message="User is not in correct step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID.value,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except SelfieNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND.value, message=msg_error
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (ErrorOnSendAuditLog, ErrorSendingToIaraValidateSelfie) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message="Invalid, extra or missing params",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR.value, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
