class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::selfie::Fail when trying to get unique id,"
        " jwt not decoded successfully"
    )


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::Audit::register_log::Error when trying to send log audit on Persephone"


class ErrorSendingToIaraValidateSelfie(Exception):
    msg = "Jormungandr-Onboarding::BureauApiTransport::create_transaction::Error when trying to send selfie to validation in Iara"


class SelfieNotExists(Exception):
    msg = "Jormungandr-Onboarding::SelfieService::_content_exists::Not found any content in bucket path"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::get_user_current_step::Error when trying to get onboarding steps br"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User is not in the electronic signature step"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"
