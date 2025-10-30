from enum import Enum, auto


class Couleur(Enum):
    ROUGE = "Rouge"
    VERT = "Vert"
    BLEU = "Bleu"


print(Couleur.ROUGE)
print(Couleur.ROUGE.name)
print(Couleur.ROUGE.value)

class Status(Enum):
    EN_ATTENTE = auto()
    EN_COURS = auto()
    TERMINE = auto()

print(list(Status))