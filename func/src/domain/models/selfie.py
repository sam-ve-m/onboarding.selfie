from dataclasses import dataclass

from src.domain.validators.validator import DeviceInformation


@dataclass
class Selfie:
    file_path: str
    unique_id: str
    device_info: DeviceInformation

    def audit_template(self) -> dict:
        template = {
            "file_path": self.file_path,
            "unique_id": self.unique_id,
            "device_info": self.device_info.dict(),
        }
        return template

    def bureau_callback_template(self) -> dict:
        template = {
            "unique_id": self.unique_id,
            "device_info": self.device_info.dict(),
        }
        return template

