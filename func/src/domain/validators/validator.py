# Third party
from pydantic import BaseModel, validator

# Standards
from re import match


class SelfieInput(BaseModel):
    device_info: str
    latitude: float
    longitude: float
    precision: float
    ip_address: str
    content: str

    @validator("content")
    def validate_content(cls, content):
        base_64_regex = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
        if match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")


class DeviceInformation(BaseModel):
    dt: int
    cm_fl: bool
    mp: int
    cm_num: int
    p_count: int
    acc_n: str
    acc_v: str
    bd: str
    hw: str
    md: str
    boa: str
    cpu: str
    md_name: str
    p_mem: int
    nfc: bool
    bio: bool
    iim: str
