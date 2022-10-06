# Third party
from unittest.mock import patch

import pytest

from src.domain.validators.validator import Base64File, DeviceInformation


# Standards


@patch.object(DeviceInformation, "__init__", return_value=None)
def test_from_request_without_geolocation(mocked_validator):
    with pytest.raises(ValueError):
        DeviceInformation.from_request({})
    mocked_validator.assert_not_called()


@patch.object(DeviceInformation, "__init__", return_value=None)
def test_from_request_with_wrong_geolocation(mocked_validator):
    with pytest.raises(ValueError):
        DeviceInformation.from_request({"geolocation": "Rua Jose da Veiga Vale, 77"})
    mocked_validator.assert_not_called()


@patch.object(DeviceInformation, "__init__", return_value=None)
def test_from_request(mocked_validator):
    DeviceInformation.from_request({"geolocation": "123, 321, 123"})
    mocked_validator.assert_called()


def test_validate_content():
    Base64File.validate_content("")


def test_validate_content_invalid():
    with pytest.raises(ValueError):
        Base64File.validate_content("|")
