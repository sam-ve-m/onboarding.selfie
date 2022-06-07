# Jormungandr - Onboarding
from ..domain.enums.types import UserFileType, FileExtensionType
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit

# Standards
from base64 import b64decode
from io import BytesIO, SEEK_SET
from typing import Union


class SelfieService:

    @staticmethod
    async def save_user_selfie(selfie_validated, unique_id):
        file_path = f"{unique_id}/{UserFileType.SELFIE}/{UserFileType.SELFIE}{FileExtensionType.SELFIE_EXTENSION}"
        temp_file = await SelfieService._resolve_content(selfie_validated=selfie_validated)
        upload_result = FileRepository.save_user_file(file_path=file_path, temp_file=temp_file)
        print(dir(upload_result))
        await Audit.register_log(file_path=file_path, unique_id=unique_id)
        return True

    @staticmethod
    async def _resolve_content(selfie_validated: Union[str, bytes]) -> BytesIO:
        if type(selfie_validated) is str:
            base64_bytes = selfie_validated.encode("ascii")
            selfie_validated = b64decode(base64_bytes)
        temp_file = BytesIO()
        temp_file.write(selfie_validated)
        temp_file.seek(SEEK_SET)
        return temp_file
