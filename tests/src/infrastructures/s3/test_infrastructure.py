from unittest.mock import patch, MagicMock

import aioboto3
import pytest
from decouple import AutoConfig

from src.infrastructures.s3.infrastructure import S3Infrastructure

dummy_env = "env"


@pytest.mark.asyncio
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_get_session(mocked_env, monkeypatch):
    dummy_connection = "dummy connection"
    mock_connection = MagicMock(return_value=dummy_connection)
    monkeypatch.setattr(aioboto3, "Session", mock_connection)

    new_connection_created = await S3Infrastructure._get_session()
    assert new_connection_created == dummy_connection
    mock_connection.assert_called_once_with(
        aws_access_key_id=dummy_env,
        aws_secret_access_key=dummy_env,
        region_name=dummy_env,
    )
    mocked_env.assert_called()

    reused_client = await S3Infrastructure._get_session()
    assert reused_client == new_connection_created
    mock_connection.assert_called_once_with(
        aws_access_key_id=dummy_env,
        aws_secret_access_key=dummy_env,
        region_name=dummy_env,
    )
    mocked_env.assert_called()
    S3Infrastructure.client = None


