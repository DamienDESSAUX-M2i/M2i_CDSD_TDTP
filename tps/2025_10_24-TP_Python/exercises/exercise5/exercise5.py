from math import ceil


def user_input(msg: str, msg_error: str) -> int:
    """Allow a user to enter an natural integer.

    Args:
        msg (str): Message to display.
        msg_error (str): Error message to display.

    Returns:
        int: The value entered by the user.
    """
    nb: int = 0
    while True:
        user_input: str = input(msg)
        try:
            nb: int = int(user_input)
            if nb > 0:
                return nb
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)


# This function needs to be improved
def is_prime_number(n: int) -> tuple[bool]:
    """Checks if a natural number is a prime number.

    Args:
        n (int): A natural number greater or equal to 1.

    Returns:
        tuple[bool]: True if 'n' is a natural number.
    """
    for p in range(2, ceil(n / 2)):
        if n % p == 0:
            return False
    return True


def main() -> None:
    """Main function"""
    msg: str = "Saisir un entier naturel supérieur à 1 : "
    msg_error: str = "Errreur de saisie. Veuillez recommencer."
    n: int = user_input(msg=msg, msg_error=msg_error)
    print(f"{n} est premier." if is_prime_number(n=n) else f"{n} n'est pas premier.")


if __name__ == "__main__":
    main()
