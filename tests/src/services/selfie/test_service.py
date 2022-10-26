from io import BufferedRandom
from unittest.mock import patch, MagicMock
from decouple import AutoConfig
import pytest


with patch.object(AutoConfig, "__init__"):
    with patch.object(AutoConfig, "__call__"):
        from func.src.domain.enums.types import UserFileType, FileExtensionType, UserOnboardingStep, UserAntiFraudStatus
        from func.src.domain.exceptions.exceptions import (
            SelfieNotExists,
            InvalidOnboardingCurrentStep, InvalidOnboardingAntiFraud,
)
        from func.src.domain.models.selfie import Selfie
        from func.src.services.selfie import SelfieService
        from func.src.transports.device_info.transport import DeviceSecurity
        from tests.src.services.selfie.image import dummy_b64
        from tests.src.services.selfie.stubs import stub_content
        from func.src.transports.onboarding_steps.transport import OnboardingSteps


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.FileRepository.list_contents", return_value=stub_content
)
async def test_when_content_exists_then_return_true(mock_list_contents, monkeypatch):
    monkeypatch.setattr(SelfieService, "_selfie_file_path_end", "Contents")
    result = await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.selfie.FileRepository.list_contents", return_value=stub_content
)
async def test_when_content_exists_then_proceed(mock_list_contents, monkeypatch):
    monkeypatch.setattr(SelfieService, "_selfie_file_path_end", "Contents")
    await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")

    mock_list_contents.assert_called_once_with(file_path="path/path/user_selfie.jpg")


@pytest.mark.asyncio
@patch("func.src.services.selfie.FileRepository.list_contents", return_value=stub_content)
async def test_when_return_empty_dict_then_raises(mock_list_contents, monkeypatch):
    monkeypatch.setattr(SelfieService, "_selfie_file_path_end", "Wrong")
    with pytest.raises(SelfieNotExists):
        await SelfieService._content_exists(file_path="path/path/user_selfie.jpg")


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(DeviceSecurity, "decrypt_device_info")
@patch.object(DeviceSecurity, "generate_device_id")
@patch.object(Selfie, "__init__", return_value=None)
@patch.object(SelfieService, "_save_selfie")
async def test_save_user_selfie(
    mocked_service, mocked_model, mocked_transport_for_id,
    mocked_transport_for_info
):
    result = await SelfieService.save_user_selfie(
        selfie_validated=dummy_value, unique_id=str(dummy_value)
    )
    file_path = f"{dummy_value}/{UserFileType.SELFIE}/{UserFileType.SELFIE}{FileExtensionType.SELFIE_EXTENSION}"

    mocked_transport_for_id.assert_called_once_with(dummy_value.device_info)
    mocked_transport_for_info.assert_called_once_with(dummy_value.device_info)
    mocked_model.assert_called_once_with(
        file_path=file_path,
        unique_id=str(dummy_value),
        device_id=mocked_transport_for_id.return_value,
        device_info=mocked_transport_for_info.return_value,
        content=dummy_value.content,
        latitude=dummy_value.latitude,
        longitude=dummy_value.longitude,
        precision=dummy_value.precision,
        ip_address=dummy_value.ip_address,
    )
    mocked_service.assert_called_once()
    assert result is True


@pytest.mark.asyncio
async def test_when_image_as_str_then_return_temp_file():
    result = await SelfieService._resolve_content(content=dummy_b64)
    assert isinstance(result, BufferedRandom)
    assert result.__sizeof__() == 4248


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step_invalid_step(mocked_transport):
    mocked_transport.return_value.step = None
    with pytest.raises(InvalidOnboardingCurrentStep):
        await SelfieService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step_invalid_anti_fraud(mocked_transport):
    mocked_transport.return_value.step = UserOnboardingStep.SELFIE
    mocked_transport.return_value.anti_fraud = UserAntiFraudStatus.REPROVED
    with pytest.raises(InvalidOnboardingAntiFraud):
        await SelfieService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)


@pytest.mark.asyncio
@patch.object(OnboardingSteps, "get_user_current_step")
async def test_validate_current_onboarding_step(mocked_transport):
    mocked_transport.return_value.step = UserOnboardingStep.SELFIE
    mocked_transport.return_value.anti_fraud = None
    result = await SelfieService.validate_current_onboarding_step(dummy_value)
    mocked_transport.assert_called_once_with(jwt=dummy_value)
    assert result is True
