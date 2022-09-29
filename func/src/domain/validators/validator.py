# Third party
from pydantic import BaseModel, validator

# Standards
from re import match


class DeviceInformation(BaseModel):
    device_id: str
    device_name: str
    device_model: str
    is_emulator: bool
    device_operating_system_name: str
    os_sdk_version: str
    device_is_in_root_mode: bool
    device_network_interfaces: str
    public_ip: str
    access_ip: str
    latitude: float
    longitude: float
    precision: float

    @classmethod
    def from_request(cls, request: dict):
        geolocation = request.get("geolocation")
        if not geolocation:
            raise ValueError(
                f"Missing Parameters in geolocation, expected: latitude,longitude,precision."
            )
        latitude_longitude_precision = geolocation.split(", ")
        if not len(latitude_longitude_precision) == 3:
            raise ValueError(
                f"Missing Parameters in geolocation: {geolocation}; "
                + "expected: latitude,longitude,precision."
            )
        request["latitude"], request["longitude"], request["precision"] = (
            map(float, latitude_longitude_precision)
        )
        del request["geolocation"]
        return cls(**request)


class Base64File(BaseModel):
    content: str
    device_info: DeviceInformation

    @validator("content", always=True)
    def validate_content(cls, content):
        base_64_regex = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")

    @classmethod
    def from_request(cls, request: dict):
        request["device_info"] = DeviceInformation.from_request(
            request.get("device_info")
        )
        return cls(**request)
