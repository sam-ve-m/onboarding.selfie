class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error when trying to send log audit on Persephone"


class ErrorOnUpdateUser(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error on trying to update user in mongo_db::" \
          "User not exists, or unique_id invalid"
