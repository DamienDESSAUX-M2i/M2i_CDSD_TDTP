class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.livres = []
        self.membres = []
    
    def ajouter_livre(self, livre):
        """Ajoute un livre au catalogue"""
        self.livres.append(livre)
    
    def ajouter_membre(self, membre):
        """Ajoute un membre à la bibliothèque"""
        self.membres.append(membre)
    
    def trouver_livre_par_isbn(self, isbn):
        """Recherche un livre par son ISBN"""
        for livre in self.livres:
            if livre.isbn == isbn:
                return livre
        return None
    
    def trouver_membre_par_numero(self, numero):
        """Recherche un membre par son numéro"""
        for membre in self.membres:
            if membre.numero_membre == numero:
                return membre
        return None
    
    def get_livres_disponibles(self):
        """Retourne la liste des livres disponibles"""
        return [livre for livre in self.livres if livre.disponible]