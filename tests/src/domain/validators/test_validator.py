import pytest

from src.domain.validators.validator import SelfieInput


def test_validate_content():
    SelfieInput.validate_content("")


def test_validate_content_invalid():
    with pytest.raises(ValueError):
        SelfieInput.validate_content("|")
