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


def display_tree(n: int) -> None:
    """Display a tree.

    Args:
        n (int): The height of the tree.
    """
    for k in range(n):
        line: str = " " * (n - 1 - k) + "*" * (1 + 2 * k)
        print(line)


def main() -> None:
    """Main function"""
    msg: str = "Saissir un nombre entier strictement positif : "
    msg_error: str = "Errreur de saisie. Veuillez recommencer."
    n: int = user_input(msg=msg, msg_error=msg_error)
    display_tree(n=n)


if __name__ == "__main__":
    main()
