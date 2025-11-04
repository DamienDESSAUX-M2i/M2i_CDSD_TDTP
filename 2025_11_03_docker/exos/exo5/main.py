from pathlib import Path
import csv


class LoginException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
    
    def display_error(self):
        print(self.msg)


class PassWordException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
    
    def display_error(self):
        print(self.msg)


def user_input_login() -> str:
    user_input: str = input("Nom utilisateur : ")
    return user_input

def user_input_password() -> str:
    user_input: str = input("Mot de passe : ")
    return user_input

def check_login(user_login: str, expected_login: str) -> None:
    if user_login != expected_login:
        raise LoginException("Nom utilisateur incorrect !")

def check_password(user_password: str, expected_password: str) -> None:
    if user_password != expected_password:
        raise PassWordException("Password incorrect !")

def login(expected_login: str, expected_password: str) -> None:
    while True:
        user_login: str = user_input_login()
        user_password: str = user_input_password()
        try:
            check_login(user_login=user_login, expected_login=expected_login)
            check_password(user_password=user_password, expected_password=expected_password)
            print("=== Login accepté ===")
            break
        except LoginException as e:
            e.display_error()
        except PassWordException as e:
            e.display_error()

def main():
    expected_login: str = "admin"
    expected_password: str = "admin"
    login(expected_login=expected_login, expected_password=expected_password)



if __name__ == "__main__":
    main()