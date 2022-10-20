import pytest

from src.domain.validators.validator import Base64File


def test_validate_content():
    Base64File.validate_content("")


def test_validate_content_invalid():
    with pytest.raises(ValueError):
        Base64File.validate_content("|")
