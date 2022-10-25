from func.src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk
from func.src.transports.onboarding_steps.transport import OnboardingSteps
from decouple import AutoConfig
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

import pytest

from func.src.domain.models.onboarding import Onboarding


dummy_value = MagicMock()


def raise_second(*args):
    if isinstance(args[1], Exception):
        raise args[1]


@pytest.mark.asyncio
@patch.object(AutoConfig, "__call__")
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Onboarding, "__init__", return_value=None)
async def test_when_success_to_get_onboarding_steps_then_returns_current_step(
        mocked_model,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
        mocked_env
):
    mocked_client_enter.return_value.get.return_value = MagicMock()
    mocked_client_enter.return_value.get.return_value.status_code = 200
    await OnboardingSteps.get_user_current_step(jwt=dummy_value)
    mocked_client_enter.return_value.get.assert_called_once_with(
        mocked_env.return_value, headers={"x-thebes-answer": dummy_value}
    )
    mocked_model.assert_called_once_with(
        step=(
            mocked_client_enter.return_value
            .get.return_value
            .json.return_value
            .get.return_value
            .get.return_value
        ),
        anti_fraud=(
            mocked_client_enter.return_value
            .get.return_value
            .json.return_value
            .get.return_value
            .get.return_value
        ),
    )


@pytest.mark.asyncio
@patch.object(AutoConfig, "__call__")
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Onboarding, "__init__", return_value=None)
async def test_when_success_to_get_onboarding_steps_then_raises(
        mocked_model,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
        mocked_env
):
    mocked_client_enter.return_value.get.return_value = MagicMock()
    mocked_client_enter.return_value.get.return_value.status_code = 500
    with pytest.raises(OnboardingStepsStatusCodeNotOk):
        await OnboardingSteps.get_user_current_step(jwt=dummy_value)
    mocked_client_enter.return_value.get.assert_called_once_with(
        mocked_env.return_value, headers={"x-thebes-answer": dummy_value}
    )
    mocked_model.assert_not_called()
