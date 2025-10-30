import random


def generator() -> str:
    """Generate an alphabetic character.

    Returns:
        str: An alphabetic character.
    """
    characters: str = "azertyuiopqsdfghjklmwxcvbn"
    return characters[random.randint(0, len(characters) - 1)]


def menu(msg: str, msg_error: str) -> None:
    """Allow a user generate an alphabetic character.

    Args:
        msg (str): Message to display.
        msg_error (str): Error message to display.
    """
    while True:
        user_input: str = input(msg)
        match user_input:
            case "1":
                print(generator().upper())
            case "2":
                print(generator().lower())
            case "3":
                exit()
            case _:
                print(msg_error)


def main() -> None:
    """Main function"""
    msg = "[1] Pour obtenir une lettre majuscule\n[2] Pour obtenir une lettre minuscule\n[3] pour quitter.\n=> "
    msg_error = "Saisie incorrecte. Veuillez recommencer."
    menu(msg=msg, msg_error=msg_error)


if __name__ == "__main__":
    main()
