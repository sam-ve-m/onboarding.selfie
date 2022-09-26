# Jormungandr - Onboarding
from ..domain.enums.types import UserFileType, FileExtensionType, UserOnboardingStep
from ..domain.exceptions.exceptions import SelfieNotExists, InvalidOnboardingCurrentStep
from ..domain.validators.validator import Base64File
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit
from ..transports.bureau_validation.transport import BureauApiTransport
from ..transports.onboarding_steps.transport import OnboardingSteps

# Standards
from base64 import b64decode
from io import SEEK_SET
from tempfile import TemporaryFile

# Third party
from decouple import config


class SelfieService:
    @staticmethod
    async def validate_current_onboarding_step(jwt: str) -> bool:
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=jwt)
        if not user_current_step == UserOnboardingStep.SELFIE:
            raise InvalidOnboardingCurrentStep
        return True

    @staticmethod
    async def save_user_selfie(selfie_validated: Base64File, unique_id: str) -> bool:
        file_path = f"{unique_id}/{UserFileType.SELFIE}/{UserFileType.SELFIE}{FileExtensionType.SELFIE_EXTENSION}"
        await Audit.record_message_log(file_path=file_path, unique_id=unique_id)
        temp_file = await SelfieService._resolve_content(
            selfie_validated=selfie_validated
        )
        await FileRepository.save_user_file(file_path=file_path, temp_file=temp_file)
        await SelfieService._content_exists(file_path=file_path)
        await BureauApiTransport.create_transaction(unique_id=unique_id)
        return True

    @staticmethod
    async def _resolve_content(selfie_validated: Base64File) -> TemporaryFile:
        content = selfie_validated.content
        decoded_selfie = b64decode(content)
        temp_file = TemporaryFile()
        temp_file.write(decoded_selfie)
        temp_file.seek(SEEK_SET)
        return temp_file

    @staticmethod
    async def _content_exists(file_path: str) -> bool:
        content_result = await FileRepository.list_contents(file_path=file_path)
        if content_result is None or config("CONTENTS") not in content_result:
            raise SelfieNotExists
        return True
