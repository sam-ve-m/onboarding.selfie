# Jormungandr - Onboarding
import asyncio

from ..domain.enums.types import UserFileType, FileExtensionType, UserOnboardingStep
from ..domain.exceptions.exceptions import SelfieNotExists, InvalidOnboardingCurrentStep
from ..domain.models.selfie import Selfie
from ..domain.validators.validator import SelfieInput
from ..repositories.mongo_db.user.repository import UserRepository
from ..repositories.s3.repository import FileRepository
from ..transports.audit.transport import Audit
from ..transports.bureau_validation.transport import BureauApiTransport
from ..transports.device_info.transport import DeviceSecurity
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
    async def save_user_selfie(selfie_validated: SelfieInput, unique_id: str) -> bool:
        file_path = f"{unique_id}/{UserFileType.SELFIE}/{UserFileType.SELFIE}{FileExtensionType.SELFIE_EXTENSION}"
        request_device_info = DeviceSecurity.decrypt_device_info(selfie_validated.device_info)
        request_device_id = DeviceSecurity.generate_device_id(selfie_validated.device_info)
        device_info, device_id = await asyncio.gather(request_device_info, request_device_id)
        selfie = Selfie(
            file_path=file_path,
            unique_id=unique_id,
            device_id=device_id,
            device_info=device_info,
            content=selfie_validated.content,
            latitude=selfie_validated.latitude,
            longitude=selfie_validated.longitude,
            precision=selfie_validated.precision,
            ip_address=selfie_validated.ip_address,
        )
        await SelfieService._save_selfie(selfie)
        return True

    @staticmethod
    async def _save_selfie(selfie: Selfie):
        await Audit.record_message_log(selfie=selfie)
        temp_file = await SelfieService._resolve_content(selfie.content)
        await FileRepository.save_user_file(file_path=selfie.file_path, temp_file=temp_file)
        await SelfieService._content_exists(file_path=selfie.file_path)
        await BureauApiTransport.create_transaction(selfie=selfie)
        await UserRepository.update_one(unique_id=selfie.unique_id, update=selfie.user_template())

    @staticmethod
    async def _resolve_content(content: str) -> TemporaryFile:
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
