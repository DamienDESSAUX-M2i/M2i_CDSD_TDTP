from livre import Livre
from magazine import Magazine
from exceptions import DocumentDejaEmprunteException, DocumentNonEmprunteException, DocumentNotExitsException


class Actions:
    def __init__(self, documents: list[Livre|Magazine]):
        self.documents: list[Livre|Magazine] = documents
    
    def user_input_title(self, msg: str) -> Livre|Magazine:
        user_input = input(msg)
        for document in self.documents:
            if document.titre == user_input:
                return document
        raise DocumentNotExitsException(f"Aucun document ne posède la titre {user_input}")

    def consulter_document(self) -> None:
        try:
            document: Livre|Magazine = self.user_input_title(msg="Donner le nom du livre que vous voulez consulter : ")
            document.consulter()
        except DocumentNotExitsException as e:
            e.display_message_error()

    def afficher_documents(self) -> None:
        print("=== Infos des documents ===")
        for document in self.documents:
            document.afficher_infos()

    def emprunter(self, livre: Livre):
        try:
            livre.emprunter()
        except DocumentDejaEmprunteException as e:
            e.display_message_error()
        else:
            print("Empunt réussi !")

    def emprunter_livre(self):
        print("=== Emprunt ===")
        try:
            livre: Livre = self.user_input_title(msg="Donner le nom du livre que vous voulez emprunter : ")
            self.emprunter(livre=livre)
        except DocumentNotExitsException as e:
            e.display_message_error()

    def rendre(self, livre: Livre):
        try:
            livre.rendre()
        except DocumentNonEmprunteException as e:
            e.display_message_error()
        else:
            print("Redu réussi !")

    def rendre_livre(self):
        print("=== Rendu ===")
        try:
            livre: Livre = self.user_input_title(msg="Donner le nom du livre que vous voulez rendre : ")
            self.rendre(livre=livre)
        except DocumentNotExitsException as e:
            e.display_message_error()