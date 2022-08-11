# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_SELFIE = 5

    def __repr__(self):
        return self.value


class UserFileType(StrEnum):
    SELFIE = "user_selfie"


class FileExtensionType(StrEnum):
    SELFIE_EXTENSION = ".jpg"


class UserOnboardingStep(StrEnum):
    SELFIE = "selfie"
