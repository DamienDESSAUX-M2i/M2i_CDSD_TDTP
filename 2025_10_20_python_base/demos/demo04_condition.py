my_var: int = 2

# if / elif / else
if my_var == 1:
    print("une\n")
elif my_var == 2:
    print("deux\n")
else:
    print("ni une, ni deux\n")

# elif et else sont facultatifs
if my_var < 3:
    print("Plus petit que 3\n")

# /!\ à la hiérarchie des condition
if my_var >= 0:
    print(">= 0\n")
elif my_var >= 1:   # On ne rentre jamais dans le sinon si
    print(">= 1\n")
else:
    print("<= 0\n")

# Ternaires
result = "0\n" if my_var == 0 else "1\n" if my_var == 1 else "> 1\n"
# équivalent à la structure imbriquée suivante (à proscrire)
if my_var == 0:
    result = "0\n"
else:
    if my_var == 1:
        result = "1\n"
    else:
        result = "> 1\n"

# in / not in
voyelles = "aeiouy"
lettre = 'y'
if lettre in voyelles:
    print("voyelle\n")
else:
    print("consonne\n")

# type versus isinstance
class A:
    pass
class B(A):
    pass
a=A()
b=B()
print(f"{type(b) == A = }\n{type(b) == B = }\n{isinstance(b,A) = }\n{isinstance(b,B) = }\n")

# match / case
test: bool = False
match my_var:
    case 0:
        print("my_var est égal 0\n")
    case 1 | 2 | 3 if test == True:
        print("Si test vaut True alors le cas 1 | 2 | 3 est pris en compte\n")
    case 4 | 5:
        print("my_var est 4 ou 5")
    case nb if nb in [6, 7, 8]:
        print("my_var est dans la liste [6, 7, 8]")
    case str():
        print("my_var est est de type str\n")
    case _: # A mettre à la fin
        print("autre chose\n")

# match / case regex
import re

class regex_in:
    def __init__(self, my_str:str):
        self.my_str: str = my_str

    def __eq__(self, other: str | re.Pattern):
        if isinstance(other, str):
            other: re.Pattern = re.compile(other)
        assert isinstance(other, re.Pattern)
        return other.fullmatch(self.my_str) is not None

match regex_in(str(my_var)):
    case r'\d+':
        print("Digits\n")
    case r'\s+':
        print("Whitespaces\n")
    case _:
        print("Something else\n")