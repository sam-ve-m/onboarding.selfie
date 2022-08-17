# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from httpx import AsyncClient
from decouple import config


class OnboardingSteps:
    @staticmethod
    async def get_user_current_step(jwt: str) -> str:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(
                config("ONBOARDING_STEPS_BR_URL"), headers=headers
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise OnboardingStepsStatusCodeNotOk
            user_current_step = (
                request_result.json().get("result", {}).get("current_step")
            )
        return user_current_step
