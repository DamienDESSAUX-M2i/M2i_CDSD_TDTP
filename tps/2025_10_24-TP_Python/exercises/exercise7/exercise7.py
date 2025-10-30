def user_input(msg: str, msg_error: str) -> int:
    """Allow a user to enter an natural integer greater than 0.

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


# Recursive function.
## Caution: If the user gives a large number, the memory allocated to the program may be exceeded.
def factorial(n: int) -> int:
    """Compute the factorial of n

    Args:
        n (int): A natural number greater than 0.

    Returns:
        int: n!
    """
    if n == 1:
        return n
    else:
        return n * factorial(n - 1)


def main() -> None:
    """Main function"""
    msg: str = "Saissir un nombre entier strictement positif : "
    msg_error: str = "Errreur de saisie. Veuillez recommencer."
    n: int = user_input(msg=msg, msg_error=msg_error)
    print(f"{n}! = {factorial(n=n)}")


if __name__ == "__main__":
    main()
