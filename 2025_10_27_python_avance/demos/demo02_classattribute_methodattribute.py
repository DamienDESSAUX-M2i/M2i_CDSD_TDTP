class Voiture:
    NB_VOITURE = 0
    INSTANCES: list['Voiture'] = []

    def __init__(self, marque, modele, couleur):
        self.marque = marque
        self.modele = modele
        self.couleur = couleur
        Voiture.NB_VOITURE += 1
        Voiture.INSTANCES.append(self)
    
    def presentation(self):
        print(f"{self.marque} - {self.modele} - {self.couleur}")

    @classmethod
    def afficher_voitures(cls):
        print("=== Voitures ===")
        for voiture in cls.INSTANCES:
            voiture.presentation()
        
    @staticmethod
    def is_marque(marque):
        return marque.lower() in ["renault", "citroen"]

voiture1 = Voiture("Renault", "21", "Bleu")
voiture2 = Voiture("Ford", "Mondeo", "Rouge")

print(f"{voiture1.NB_VOITURE = }\n{voiture2.NB_VOITURE = }\n{Voiture.NB_VOITURE = }")
Voiture.afficher_voitures()

print(Voiture.is_marque("Renault"))