def get_positive_int(message: str) -> int:
    user_input: str = input(message)
    try:
        user_input: int = int(user_input)
        if user_input < 1:
            raise ValueError("'user_input' must be greater than or equal to 1.")
        return user_input
    except ValueError:
        print("Erreur : La saisie doit être un nombre entier supérieur ou égal à 1.")


def get_str(message: str) -> str:
    return input(message)


def get_email(message: str) -> str:
    pass


if __name__ == "__main__":
    print(get_positive_int(message="ID : "))
