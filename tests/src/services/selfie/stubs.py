from unittest.mock import patch
from decouple import AutoConfig

with patch.object(AutoConfig, "__call__"):
    from func.src.domain.validators.validator import SelfieInput
from tests.src.services.selfie.image import payload_b64_file

stub_content = {"Contents": {"test": "test"}}
stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_b64_file = SelfieInput(**payload_b64_file)
