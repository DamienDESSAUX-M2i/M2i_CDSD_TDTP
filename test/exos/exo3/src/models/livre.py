class Livre:
    def __init__(self, titre, auteur, isbn, disponible=True):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.disponible = disponible
    
    def emprunter(self):
        """Marque le livre comme non disponible"""
        if self.disponible:
            self.disponible = False
            return True
        return False
    
    def retourner(self):
        """Marque le livre comme disponible"""
        if not self.disponible:
            self.disponible = True
            return True
        return False
    
    def get_info(self):
        """Retourne les informations du livre"""
        return f"{self.titre} par {self.auteur} (ISBN: {self.isbn})"