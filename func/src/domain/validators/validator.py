# Third party
from pydantic import BaseModel, validator

# Standards
from re import match
from decouple import config


class SelfieInput(BaseModel):
    device_info: str
    latitude: float
    longitude: float
    precision: float = float(config("DEFAULT_PRECISION_VALUE"))
    ip_address: str
    content: str

    @validator("content")
    def validate_content(cls, content):
        base_64_regex = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")
