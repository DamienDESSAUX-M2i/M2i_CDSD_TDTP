from document import Document
from empruntable import Empruntable
from consultable import Consultable
from genre import Genre
from exceptions import DocumentDejaEmprunteException, DocumentNonEmprunteException


class Livre(Document, Empruntable, Consultable):
    INTANCES_LIVRE: list['Livre'] = []

    def __init__(self, titre: str, annee_publication: int, auteur: str, nb_pages: int, genre: Genre):
        Document.__init__(self, titre, annee_publication)
        Empruntable.__init__(self, est_emprunte=False)
        Livre.INTANCES_LIVRE.append(self)
        self.auteur: str = auteur
        self.nb_pages: int = nb_pages
        self.genre: Genre = genre
    
    def afficher_infos(self) -> None:
        print("=== Livre ===")
        Document.afficher_infos(self)
    
    def emprunter(self) -> None:
        if not self.est_emprunte:
            self.est_emprunte = True
        else:
            raise DocumentDejaEmprunteException(f"Le livre intitulé {self.titre} est déjà emprunté.")

    def rendre(self) -> None:
        if self.est_emprunte:
            self.est_emprunte = False
        else:
            raise DocumentNonEmprunteException(f"Le livre intitulé {self.titre} n'a pas été emprunté et ne peut être rendu.")

    def consulter(self) -> None:
        print(f"Vous consulter le livre intitulé {self.titre}")

    @staticmethod
    def livre(titre: str, auteur: str, genre: Genre) -> 'Livre':
        return Livre(titre=titre, annee_publication=0, auteur=auteur, nb_pages=0, genre=genre)

    @staticmethod
    def compteur_pages(livres: list['Livre']) -> int:
        return sum([livre.nb_pages for livre in livres])