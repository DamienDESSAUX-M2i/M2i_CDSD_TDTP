class Membre:
    def __init__(self, nom, prenom, numero_membre, limite_emprunts=3):
        self.nom = nom
        self.prenom = prenom
        self.numero_membre = numero_membre
        self.livres_empruntes = []
        self.limite_emprunts = limite_emprunts
    
    def peut_emprunter(self):
        """Vérifie si le membre peut emprunter un livre"""
        return len(self.livres_empruntes) < self.limite_emprunts
    
    def emprunter_livre(self, livre):
        """Ajoute un livre à la liste des emprunts"""
        if self.peut_emprunter():
            self.livres_empruntes.append(livre)
            return True
        return False
    
    def retourner_livre(self, livre):
        """Retire un livre de la liste des emprunts"""
        if livre in self.livres_empruntes:
            self.livres_empruntes.remove(livre)
            return True
        return False
    
    def get_nombre_emprunts(self):
        """Retourne le nombre de livres empruntés"""
        return len(self.livres_empruntes)
    
    def get_nom_complet(self):
        """Retourne le nom complet du membre"""
        return f"{self.prenom} {self.nom}"