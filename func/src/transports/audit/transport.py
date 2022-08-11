# Jormungandr - Onboarding
from ...domain.exceptions import ErrorOnSendAuditLog
from ...domain.enums.types import QueueTypes

# Third party
from decouple import config
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def register_log(cls, unique_id: str, file_path: str):
        message = {
            "unique_id": unique_id,
            "file_path": file_path,
        }
        partition = QueueTypes.USER_SELFIE
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_USER_SELFIE")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            raise ErrorOnSendAuditLog
