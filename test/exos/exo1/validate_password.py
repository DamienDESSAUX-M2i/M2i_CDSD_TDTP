import re


def validate_password(password: str) -> bool:
    """
    Validate whether a password meets basic complexity requirements.

    The password must:
    - Be at least 8 characters long
    - Contain at least one lowercase letter
    - Contain at least one uppercase letter
    - Contain at least one digit
    - Contain at least one special character

    Args:
        password (str): The password string to validate.

    Returns:
        bool: True if the password satisfies all requirements, False otherwise.
    """
    if len(password) < 8:
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True
