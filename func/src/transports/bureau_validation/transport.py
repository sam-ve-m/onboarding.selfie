from iara_client import Iara, IaraTopics

from src.domain.exceptions.exceptions import ErrorSendingToIaraValidateSelfie


class BureauApiTransport:
    @staticmethod
    async def create_transaction(unique_id: str):
        success, reason = await Iara.send_to_iara(
            topic=IaraTopics.CAF_SELFIE_VALIDATION,
            message={"unique_id": unique_id},
        )
        if not success:
            raise ErrorSendingToIaraValidateSelfie(str(reason))
