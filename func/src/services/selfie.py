# Jormungandr - Onboarding
from ..domain.enums.types import UserFileType, FileExtensionType
from ..domain.exceptions import SelfieNotExists
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit

# Standards
from base64 import b64decode
from io import SEEK_SET
from tempfile import TemporaryFile

# Third party
from decouple import config


class SelfieService:

    @staticmethod
    async def save_user_selfie(selfie_validated: dict, unique_id: str):
        file_path = f"{unique_id}/{UserFileType.SELFIE}/{UserFileType.SELFIE}{FileExtensionType.SELFIE_EXTENSION}"
        temp_file = await SelfieService._resolve_content(selfie_validated=selfie_validated)
        await FileRepository.save_user_file(file_path=file_path, temp_file=temp_file)
        await SelfieService._content_exists(file_path=file_path)
        await Audit.register_log(file_path=file_path, unique_id=unique_id)
        return True

    @staticmethod
    async def _resolve_content(selfie_validated: dict) -> TemporaryFile:
        content = selfie_validated.get("content")
        decoded_selfie = b64decode(content)
        temp_file = TemporaryFile()
        temp_file.write(decoded_selfie)
        temp_file.seek(SEEK_SET)
        return temp_file

    @staticmethod
    async def _content_exists(file_path: str):
        content_result = await FileRepository.list_contents(file_path=file_path)
        if content_result is None or config("CONTENTS") not in content_result:
            raise SelfieNotExists
