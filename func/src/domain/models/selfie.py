from dataclasses import dataclass

from src.domain.enums.types import CpfValidationStatus


@dataclass
class Selfie:
    file_path: str
    unique_id: str
    device_info: str

    def audit_template(self) -> dict:
        template = {
            "file_path": self.file_path,
            "unique_id": self.unique_id,
            "device_info": self.device_info,
        }
        return template

    def bureau_callback_template(self) -> dict:
        template = {
            "unique_id": self.unique_id,
            "device_info": self.device_info,
        }
        return template

    @staticmethod
    def user_template() -> dict:
        template = {
            "bureau_validations.score": CpfValidationStatus.QUEUED.value,
        }
        return template
