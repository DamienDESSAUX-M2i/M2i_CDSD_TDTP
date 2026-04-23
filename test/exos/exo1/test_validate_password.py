import pytest
from validate_password import validate_password


@pytest.mark.parametrize(
    "password,expected",
    [
        ("Password1!", True),
        ("Pass1!", False),
        ("PASSWORD1!", False),
        ("password1!", False),
        ("Password!", False),
        ("Password1", False),
    ],
    ids=[
        "valid_password",
        "too_short",
        "missing_lowercase",
        "missing_uppercase",
        "missing_digit",
        "missing_special_char",
    ],
)
def test_validate_password(password: str, expected: bool) -> None:
    assert validate_password(password) is expected
