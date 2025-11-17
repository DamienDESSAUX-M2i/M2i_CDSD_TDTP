class CompteBancaire():
    TAUX_AGIOS: float = 0.05
    DECOUVERT_AUTORISE: float = 0

    def __init__(
            self,
            numero_compte: int,
            nom: str,
            solde: float
            ) -> None:
        self.numero_compte: int = numero_compte
        self.nom: str = nom
        self.solde: float = solde
    
    def versement(self, other_compte: 'CompteBancaire', montant_versement: float) -> None:
        self.solde -= montant_versement
        other_compte.solde += montant_versement
    
    def retrait(self, montant_retrait: float) -> None:
        self.solde -= montant_retrait
    
    def agios(self) -> None:
        if self.solde < self.DECOUVERT_AUTORISE:
            self.solde *= (1 + self.TAUX_AGIOS)
        
    def afficher(self) -> None:
        print(f"\n=== No compte : {self.numero_compte} ===\n")
        for attribute, value in self.__dict__.items():
            print(f"{attribute} : {value}")

compte1 = CompteBancaire(numero_compte=1, nom="a", solde=100)
compte1.afficher()
compte2 = CompteBancaire(numero_compte=2, nom="b", solde=100)
compte2.afficher()
compte1.retrait(5)
compte1.afficher()
compte2.versement(compte1, 200)
compte1.afficher()
compte2.afficher()
compte2.agios()
compte2.afficher()