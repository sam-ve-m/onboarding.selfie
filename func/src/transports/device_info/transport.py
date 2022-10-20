# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import DeviceSecurityDecryptDeviceInfo, DeviceSecurityDeviceId

# Standards
from http import HTTPStatus

# Third party
from httpx import AsyncClient
from decouple import config

from ...domain.validators.validator import DeviceInformation


class DeviceSecurity:
    @staticmethod
    async def decrypt_device_info(device_info: str) -> DeviceInformation:
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DECRYPT_DEVICE_INFO_URL"), json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise DeviceSecurityDecryptDeviceInfo()
        raw_device_info = (
            request_result.json().get("deviceInfo")
        )
        device_info_model = DeviceInformation(**raw_device_info)
        return device_info_model

    @staticmethod
    async def generate_device_id(device_info: str) -> str:
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DEVICE_ID_URL"), json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise DeviceSecurityDeviceId()
        device_id = (
            request_result.json().get("deviceID")
        )
        return device_id
