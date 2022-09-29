# Jormungandr - Onboarding
from func.src.domain.exceptions.exceptions import (
    SelfieNotExists,
    ErrorOnSendAuditLog,
    InvalidOnboardingCurrentStep,
)
from func.src.services.selfie import SelfieService
from func.src.transports.bureau_validation.transport import BureauApiTransport
from tests.src.services.selfie.stubs import stub_content, stub_unique_id, stub_b64_file

# Standards
from unittest.mock import patch
from io import BufferedRandom

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.FileRepository.list_contents", return_value=stub_content
)
async def test_when_content_exists_then_return_true(mock_list_contents):
    result = await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.FileRepository.list_contents", return_value=stub_content
)
async def test_when_content_exists_then_proceed(mock_list_contents):
    await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")

    mock_list_contents.assert_called_once_with(file_path="path/path/user_selfie.jpg")


@pytest.mark.asyncio
@patch("func.src.services.selfie.FileRepository.list_contents", return_value=None)
async def test_when_content_not_exists_then_raises(mock_list_contents):
    with pytest.raises(SelfieNotExists):
        await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")


@pytest.mark.asyncio
@patch("func.src.services.selfie.FileRepository.list_contents", return_value={})
async def test_when_return_empty_dict_then_raises(mock_list_contents):
    with pytest.raises(SelfieNotExists):
        await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")


@pytest.mark.asyncio
@patch.object(SelfieService, "_content_exists")
@patch("func.src.services.selfie.FileRepository.save_user_file")
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(False, "TESTE"),
)
async def test_when_failed_to_send_audit_log_then_raises(
    mock_persephone, mock_save_user, mock_content
):
    with pytest.raises(ErrorOnSendAuditLog):
        await SelfieService.save_user_selfie(
            selfie_validated=stub_b64_file, unique_id=stub_unique_id
        )


@pytest.mark.asyncio
async def test_when_image_as_str_then_return_temp_file():
    result = await SelfieService._resolve_content(selfie_validated=stub_b64_file)

    assert isinstance(result, BufferedRandom)
    assert result.__sizeof__() == 4248


@pytest.mark.asyncio
@patch("func.src.services.selfie.Audit.record_message_log")
@patch.object(SelfieService, "_content_exists")
@patch("func.src.services.selfie.FileRepository.save_user_file")
@patch.object(BureauApiTransport, "create_transaction")
async def test_when_valid_unique_id_and_selfie_then_return_true(
    mock_validate_file, mock_save_file, mock_content_exists, mock_register_log
):
    success = await SelfieService.save_user_selfie(
        selfie_validated=stub_b64_file, unique_id=stub_unique_id
    )

    assert success is True


@pytest.mark.asyncio
@patch("func.src.services.selfie.Audit.record_message_log")
@patch.object(SelfieService, "_content_exists")
@patch("func.src.services.selfie.FileRepository.save_user_file")
@patch.object(BureauApiTransport, "create_transaction")
async def test_when_valid_unique_id_and_selfie_then_mocks_was_called(
    mock_validate_file, mock_save_file, mock_content_exists, mock_register_log
):
    await SelfieService.save_user_selfie(
        selfie_validated=stub_b64_file, unique_id=stub_unique_id
    )

    mock_save_file.assert_called_once()
    mock_content_exists.assert_called_once_with(
        file_path=f"{stub_unique_id}/user_selfie/user_selfie.jpg"
    )
    mock_register_log.assert_called_once()


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.OnboardingSteps.get_user_current_step",
    return_value="selfie",
)
async def test_when_current_step_correct_then_return_true(mock_onboarding_steps):
    result = await SelfieService.validate_current_onboarding_step(jwt="123")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.OnboardingSteps.get_user_current_step",
    return_value="finished",
)
async def test_when_current_step_invalid_then_return_raises(mock_onboarding_steps):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await SelfieService.validate_current_onboarding_step(jwt="123")
