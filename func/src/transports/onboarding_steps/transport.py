# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from httpx import AsyncClient
from decouple import config

from ...domain.models.onboarding import Onboarding


class OnboardingSteps:
    @staticmethod
    async def get_user_current_step(jwt: str) -> Onboarding:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(
                config("ONBOARDING_STEPS_BR_URL"), headers=headers
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise OnboardingStepsStatusCodeNotOk()

        result = request_result.json().get("result", {})
        user_current_step = result.get("current_step")
        user_anti_fraud = result.get("anti_fraud")
        onboarding = Onboarding(
            step=user_current_step,
            anti_fraud=user_anti_fraud,
        )
        return onboarding
