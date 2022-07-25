# Jormungandr - Onboarding
from ...domain.exceptions import ErrorOnSendAuditLog
from ...domain.enums.types import QueueTypes

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone
    partition = QueueTypes.USER_SELFIE
    topic = config("PERSEPHONE_TOPIC_USER")
    schema_name = config("PERSEPHONE_USER_SELFIE")

    @classmethod
    async def register_log(cls, unique_id: str, file_path: str):
        message = {
            "unique_id": unique_id,
            "file_path": file_path,
        }
        (
            success,
            status_sent_to_persephone
        ) = await cls.audit_client.send_to_persephone(
            topic=cls.topic,
            partition=cls.partition,
            message=message,
            schema_name=cls.schema_name,
        )
        if not success:
            Gladsheim.error(message="Audit::register_user_log::Error on trying to register log")
            raise ErrorOnSendAuditLog
