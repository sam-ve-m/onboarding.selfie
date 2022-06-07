# Third party
from pydantic import BaseModel, constr


class FileBase64(BaseModel):
    file_or_base64: constr(min_length=258)
