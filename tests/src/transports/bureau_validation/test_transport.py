from unittest.mock import MagicMock, patch

import pytest
from iara_client import Iara

from src.domain.exceptions.exceptions import ErrorSendingToIaraValidateSelfie
from src.transports.bureau_validation.transport import BureauApiTransport

stub_user = MagicMock()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_create_transaction(mocked_lib):
    mocked_lib.return_value = True, None
    await BureauApiTransport.create_transaction(stub_user)


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_create_transaction_with_errors(mocked_lib):
    dummy_value = "value"
    mocked_lib.return_value = False, dummy_value
    with pytest.raises(ErrorSendingToIaraValidateSelfie) as error:
        await BureauApiTransport.create_transaction(stub_user)
        assert str(error) == dummy_value
