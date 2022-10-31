# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import DeviceSecurityDecryptDeviceInfo, DeviceSecurityDeviceId

# Standards
from http import HTTPStatus

# Third party
from httpx import AsyncClient
from decouple import config
from etria_logger import Gladsheim


class DeviceSecurity:
    @staticmethod
    async def decrypt_device_info(device_info: str) -> dict:
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DECRYPT_DEVICE_INFO_URL"), json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                Gladsheim.error(
                    message=DeviceSecurityDecryptDeviceInfo.msg,
                    status=request_result.status_code,
                    content=request_result.content
                )
                raise DeviceSecurityDecryptDeviceInfo()
        device_info_decrypted = (
            request_result.json().get("deviceInfo")
        )
        return device_info_decrypted

    @staticmethod
    async def generate_device_id(device_info: str) -> str:
        body = {"deviceInfo": device_info}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.post(
                config("DEVICE_SECURITY_DEVICE_ID_URL"), json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                Gladsheim.error(
                    message=DeviceSecurityDeviceId.msg,
                    status=request_result.status_code,
                    content=request_result.content
                )
                raise DeviceSecurityDeviceId()
        device_id = (
            request_result.json().get("deviceID")
        )
        return device_id
