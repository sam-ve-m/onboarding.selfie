class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::selfie::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::Audit::register_log::Error when trying to send log audit on Persephone"


class SelfieNotExists(Exception):
    msg = "Jormungandr-Onboarding::SelfieService::_content_exists::Not found any content in bucket path"
