# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    USER_SELFIE = 5


class UserFileType(StrEnum):
    SELFIE = "user_selfie"


class FileExtensionType(StrEnum):
    SELFIE_EXTENSION = ".jpg"
