class InvalidLoginException(Exception):
    def __init__(self, msg: str):
        self.msg: str = msg
    
    def display_exception(self):
        print(self.msg)

class InvalidPassWordException(Exception):
    def __init__(self, msg: str):
        self.msg: str = msg
    
    def display_exception(self):
        print(self.msg)

def is_correct_login(user_input: str) -> bool:
    for character in user_input:
        if not (character.isalpha() and character.islower()):
            return False
    return True

def is_correct_password(user_input: str) -> bool:
    for character in user_input:
        if not character.isdigit():
            return False
    return True

def user_input_login() -> str:
    user_input: str = input("Veuillez entrer un login SVP (celui-ci ne doit possèder que des lettres minuscules) : ")
    if is_correct_login(user_input):
        return user_input
    raise InvalidLoginException("Le login ne doit contenir que des lettres minuscules !")

def user_input_password() -> str:
    user_input: str = input("Veuillez entrer un mot de passe SVP (celui-ci ne doit possèder que des chiffres) : ")
    if is_correct_password(user_input):
        return user_input
    raise InvalidPassWordException("Le mot de passe ne doit contient que des chiffres !")

def create_login_password() -> tuple[str]:
    while True:
        try:            
            user_login: str = user_input_login()
            user_password: str = user_input_password()
        except InvalidLoginException as e:
            e.display_exception()
        except InvalidPassWordException as e:
            e.display_exception()
        else:
            return (user_login, user_password)

def main() -> None:
    user_login, user_password = create_login_password()
    print(f"{user_login = }\n{user_password = }")


if __name__ == "__main__":
    main()