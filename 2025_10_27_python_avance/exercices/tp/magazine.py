from document import Document
from consultable import Consultable


class Magazine(Document, Consultable):
    INTANCES_MAGAZINE: list['Magazine'] = []

    def __init__(self, titre: str, annee_publication: int, numero: int):
        Document.__init__(self, titre, annee_publication)
        Magazine.INTANCES_MAGAZINE.append(self)
        self.numero: int = numero
    
    def afficher_infos(self) -> None:
        print("=== Magazine ===")
        Document.afficher_infos(self)
    
    def consulter(self) -> None:
        print(f"Vous consulter le magazine intitulé {self.titre}.")