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
            return nb
        except ValueError:
            print(msg_error)


def display_table_of_contents(nb_chapter: int, nb_section: int) -> None:
    """Display the table of contents.

    Args:
        nb_chapter (int): The number of chapters.
        nb_section (int): The number of sections.
    """
    for chapter in range(1, nb_chapter + 1):
        print(f"Chapitre {chapter}")
        for section in range(1, nb_section + 1):
            print(f"\tSous-partie {section}")


def main() -> None:
    """Main function."""
    msg_chapter: str = "Combien de chapitre voulez-vous ? "
    msg_section: str = "Combien de sous-partie voulez-vous ? "
    msg_error: str = "Errreur de saisie. Veuillez recommencer."
    nb_chapter: int = user_input(msg=msg_chapter, msg_error=msg_error)
    nb_section: int = user_input(msg=msg_section, msg_error=msg_error)
    display_table_of_contents(nb_chapter=nb_chapter, nb_section=nb_section)


if __name__ == "__main__":
    main()
