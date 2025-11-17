# match / case regex
import re

caractere: str = "a"

class regex_in:
    def __init__(self, my_str:str):
        self.my_str: str = my_str

    def __eq__(self, other: str | re.Pattern):
        if isinstance(other, str):
            other: re.Pattern = re.compile(other)
        assert isinstance(other, re.Pattern)
        return other.fullmatch(self.my_str) is not None

match regex_in(caractere):
    case r"[0-9]":
        print(f"{caractere} est chiffre")
    case r"[a-zA-Z]":
        print(f"{caractere} est une lettre")
    case _:
        print(f"{caractere} n'est ni un chiffre ni une lettre")

# Autre méthode
if caractere.isalpha():
    print(f"{caractere} est une lettre")
elif caractere.isdigit():
    print(f"{caractere} est un chiffre")
else:
    print(f"{caractere} n'est ni une lettre, ni un chiffre")