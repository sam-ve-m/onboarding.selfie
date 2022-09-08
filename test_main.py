# PROJECT IMPORTS
from http import HTTPStatus

import flask
import pytest
from unittest.mock import patch, MagicMock

from decouple import RepositoryEnv, Config
import logging.config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import selfie
                from src.services.jwt import JwtService
                from src.domain.enums.code import InternalCode
                from src.domain.response.model import ResponseModel
                from src.domain.validators.validator import Base64File
                from src.domain.exceptions.exceptions import ErrorOnDecodeJwt, ErrorOnSendAuditLog, SelfieNotExists, OnboardingStepsStatusCodeNotOk, InvalidOnboardingCurrentStep, ErrorOnGetUniqueId
                from src.services.selfie import SelfieService


error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Unauthorized token",
    HTTPStatus.UNAUTHORIZED
)
error_on_send_audit_log_case = (
    ErrorOnSendAuditLog(),
    ErrorOnSendAuditLog.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
selfie_not_exists_case = (
    SelfieNotExists(),
    SelfieNotExists.msg,
    InternalCode.DATA_NOT_FOUND,
    "Unexpected error occurred",
    HTTPStatus.BAD_REQUEST
)
onboarding_steps_status_code_not_ok_case = (
    OnboardingStepsStatusCodeNotOk(),
    OnboardingStepsStatusCodeNotOk.msg,
    InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
invalid_onboarding_current_step_case = (
    InvalidOnboardingCurrentStep(),
    InvalidOnboardingCurrentStep.msg,
    InternalCode.ONBOARDING_STEP_INCORRECT,
    "User is not in correct step",
    HTTPStatus.BAD_REQUEST
)
error_on_get_unique_id_case = (
    ErrorOnGetUniqueId(),
    ErrorOnGetUniqueId.msg,
    InternalCode.JWT_INVALID,
    "Fail to get unique_id",
    HTTPStatus.UNAUTHORIZED
)

value_exception_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid, extra or missing params",
    HTTPStatus.BAD_REQUEST
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    error_on_decode_jwt_case,
    error_on_send_audit_log_case,
    selfie_not_exists_case,
    onboarding_steps_status_code_not_ok_case,
    invalid_onboarding_current_step_case,
    error_on_get_unique_id_case,
    value_exception_case,
    exception_case,
])
@patch.object(SelfieService, "validate_current_onboarding_step")
@patch.object(SelfieService, "save_user_selfie")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(Base64File, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_selfie_raising_errors(
            mocked_build_response, mocked_response_instance, mocked_model,
            mocked_jwt_decode, mocked_logger, mocked_service, mocked_validation, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await selfie()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(SelfieService, "validate_current_onboarding_step")
@patch.object(SelfieService, "save_user_selfie", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(Base64File, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_selfie(
        mocked_build_response, mocked_response_instance, mocked_model,
        mocked_jwt_decode, mocked_logger, mocked_service, mocked_validation, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await selfie()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=dummy_response,
        code=InternalCode.SUCCESS.value,
        message='User selfie saved successfully',
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
