# Standards
from http import HTTPStatus
from unittest.mock import MagicMock, patch, AsyncMock

import pytest
# Third party
from decouple import config, Config
from etria_logger import Gladsheim
from httpx import AsyncClient

from src.domain.exceptions.exceptions import DeviceSecurityDecryptDeviceInfo, DeviceSecurityDeviceId
from src.domain.validators.validator import DeviceInformation
from src.transports.device_info.transport import DeviceSecurity


dummy_value = MagicMock()


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__")
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_generate_device_id(
        mocked_logger,
        mocked_env,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.OK
    result = await DeviceSecurity.generate_device_id(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_not_called()
    assert result == (
        mocked_client_enter.return_value.post.return_value
        .json.return_value
        .get.return_value
        )


def raise_second(*args):
    raise args[1]


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
async def test_generate_device_id_with_error(
        mocked_logger,
        mocked_env,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    with pytest.raises(DeviceSecurityDeviceId):
        await DeviceSecurity.generate_device_id(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_called_once_with(
        message=DeviceSecurityDeviceId.msg,
        status=mocked_client_enter.return_value.post.return_value.status_code,
        content=mocked_client_enter.return_value.post.return_value.content
    )


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__")
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
@patch.object(DeviceInformation, "__init__", return_value=None)
async def test_decrypt_device_info(
        mocked_model,
        mocked_logger,
        mocked_env,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.OK
    await DeviceSecurity.decrypt_device_info(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_not_called()
    mocked_model.assert_called_once()
    (
        mocked_client_enter.return_value.post.
        return_value.json.return_value
        .get.assert_called_once()
    )


def raise_second(*args):
    raise args[1]


@pytest.mark.asyncio
@patch.object(AsyncClient, "__init__", return_value=None)
@patch.object(AsyncClient, "__aenter__")
@patch.object(AsyncClient, "__aexit__", side_effect=raise_second)
@patch.object(Config, "__call__")
@patch.object(Gladsheim, "error")
@patch.object(DeviceInformation, "__init__", return_value=None)
async def test_decrypt_device_info_with_error(
        mocked_model,
        mocked_logger,
        mocked_env,
        mocked_client_exit,
        mocked_client_enter,
        mocked_client_instance,
):
    mocked_client_enter.return_value.post = AsyncMock()
    mocked_client_enter.return_value.post.return_value = MagicMock()
    mocked_client_enter.return_value.post.return_value.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    with pytest.raises(DeviceSecurityDecryptDeviceInfo):
        await DeviceSecurity.decrypt_device_info(dummy_value)
    mocked_client_enter.return_value.post.assert_called_once_with(
        mocked_env.return_value, json={"deviceInfo": dummy_value}
    )
    mocked_logger.assert_called_once_with(
        message=DeviceSecurityDecryptDeviceInfo.msg,
        status=mocked_client_enter.return_value.post.return_value.status_code,
        content=mocked_client_enter.return_value.post.return_value.content
    )
    mocked_model.assert_not_called()

