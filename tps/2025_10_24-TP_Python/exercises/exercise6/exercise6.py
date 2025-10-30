import random
from typing import TypedDict


class Msgs(TypedDict):
    """Format of a dictionary containing the messages to be displayed.

    Keys:
        msg_start (str): Message when starting the game.
        msg_less (str): Message when the given number is less than the mystery number.
        msg_greater (str): Message when the given number is greater than the mystery number.
        msg_win (str): Message when Message when the given number is equal to the mystery number.
        msg_error (str): Error message.
    """

    msg_start: str
    msg_less: str
    msg_greater: str
    msg_win: str
    msg_error: str


def user_input(a: int, b: int, msg: str, msg_error: str) -> int:
    """Allow a user to enter an natural integer between a and b.

    Args:
        a (int) : Lower bound of the interval.
        b (int) : Upper bound of the interval.
        msg (str): Message to display.
        msg_error (str): Error message to display.

    Returns:
        int: The value entered by the user.
    """
    n: int = 0
    while True:
        user_input: str = input(msg)
        try:
            n: int = int(user_input)
            if a <= n <= b:
                return n
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)


def game(a: int, b: int, mystery_number: int, msgs: Msgs) -> None:
    """Allow the user to guess a number between a and b.

    Args:
        a (int): Lower bound of the interval.
        b (int): Upper bound of the interval.
        mystery_number (int): The number to guess.
        msgs (Msgs): Dictionary containing messages to display.
    """
    nb_attempts: int = 1
    given_number: int = user_input(
        a=a, b=b, msg=msgs["msg_start"], msg_error=msgs["msg_error"]
    )
    while True:
        if given_number < mystery_number:
            given_number: int = user_input(
                a=a, b=b, msg=msgs["msg_greater"], msg_error=msgs["msg_error"]
            )
        elif given_number > mystery_number:
            given_number: int = user_input(
                a=a, b=b, msg=msgs["msg_less"], msg_error=msgs["msg_error"]
            )
        else:
            print(f"{msgs['msg_win']}{nb_attempts}")
            break
        nb_attempts += 1


def main() -> None:
    """Main function"""
    a: int = 1
    b: int = 10
    mystery_number = random.randint(a, b)

    msgs: Msgs = {}
    msgs["msg_start"] = (
        f"Je suis un nombre entier compris entre {a} et {b}. Qui suis-je ? "
    )
    msgs["msg_less"] = "Je suis plus petit. Qui sui-je ? "
    msgs["msg_greater"] = "Je suis plus grand. Qui suis-je ? "
    msgs["msg_win"] = "Bravo ! Nombre de tentative(s) : "
    msgs["msg_error"] = "Errreur de saisie. Veuillez recommencer."

    game(a=a, b=b, mystery_number=mystery_number, msgs=msgs)


if __name__ == "__main__":
    main()
