from decouple import config
from persephone_client import Persephone

from ...domain.enums.types import QueueTypes
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.models.selfie import Selfie


class Audit:
    audit_client = Persephone

    @classmethod
    async def record_message_log(cls, selfie: Selfie):
        message = selfie.audit_template()
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
        return True
