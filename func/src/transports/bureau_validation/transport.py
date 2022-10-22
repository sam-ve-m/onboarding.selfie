from iara_client import Iara, IaraTopics

from src.domain.exceptions.exceptions import ErrorSendingToIaraValidateSelfie
from src.domain.models.selfie import Selfie


class BureauApiTransport:
    @staticmethod
    async def create_transaction(selfie: Selfie):
        message = selfie.bureau_callback_template()
        success, reason = await Iara.send_to_iara(
            topic=IaraTopics.CAF_SELFIE_VALIDATION,
            message=message,
        )
        if not success:
            raise ErrorSendingToIaraValidateSelfie(str(reason))
