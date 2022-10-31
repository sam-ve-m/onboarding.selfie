from dataclasses import dataclass

from src.domain.enums.types import CpfValidationStatus


@dataclass
class Selfie:
    content: str
    file_path: str
    unique_id: str
    device_id: str
    ip_address: str
    latitude: float
    longitude: float
    precision: float
    device_info: dict

    def audit_template(self) -> dict:
        template = {
            "file_path": self.file_path,
            "unique_id": self.unique_id,
            "device_id": self.device_id,
            "device_info": self.device_info,
            "geolocation": f"{self.latitude}, {self.longitude}, {self.precision}",
            "ip_address": self.ip_address,
        }
        return template

    def bureau_callback_template(self) -> dict:
        template = {
            "unique_id": self.unique_id,
            "device_info": self.device_info,
            "device_id": self.device_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "precision": self.precision,
            "ip_address": self.ip_address,
        }
        return template

    @staticmethod
    def user_template() -> dict:
        template = {
            "bureau_validations.score": CpfValidationStatus.QUEUED.value,
        }
        return template
