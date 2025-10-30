from abc import ABC, abstractmethod


class Document(ABC):
    INTANCES: list['Document'] = []

    def __init__(self, titre: str, annee_publication: int):
        Document.INTANCES.append(self)
        self.titre: str = titre
        self.annee_publication: int = annee_publication
    
    @abstractmethod
    def afficher_infos(self) -> None:
        infos: list[str] = []
        for attribut, value in self.__dict__.items():
            infos.append(f"{attribut} : {value}")
        print("\n".join(infos))
    
    def afficher_nb_document(self) -> None:
        print(len(Document.INTANCES))