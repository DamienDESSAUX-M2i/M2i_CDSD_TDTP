class WaterTank:
    POIDS_TOTAL: float = 0
    CAPACITE_TOTAL: float = 0
    NIVEAU_REMPLISSAGE_TOTAL: float = 0

    def __init__(self, poids_vide: float, capacite_max: float, niveau_remplissage: float, masse_volumique: float = 1.0) -> None:
        self.check_poids_vide(poids_vide)
        self._poids_vide: float = poids_vide # en kg
        self.check_capacite_max(capacite_max)
        self._capacite_max: float = capacite_max # en m**3
        self.check_niveau_remplissage(niveau_remplissage)
        self._niveau_remplissage: float = niveau_remplissage # en m**3
        self.check_masse_volumique(masse_volumique)
        self._masse_volumique: float = masse_volumique # en kg/m**3
        WaterTank.POIDS_TOTAL += self._poids_vide + self._niveau_remplissage * self._masse_volumique
        WaterTank.CAPACITE_TOTAL += self._capacite_max
        WaterTank.NIVEAU_REMPLISSAGE_TOTAL += self._niveau_remplissage
    
    @property
    def poids_vide(self):
        return self._poids_vide

    @poids_vide.setter
    def poids_vide(self, poids_vide):
        self.check_poids_vide(poids_vide)
        self._poids_vide = poids_vide 

    def check_poids_vide(self, poids_vide):
        if not isinstance(poids_vide, float):
            raise TypeError(poids_vide)
        if poids_vide < 0:
            raise ValueError(f"Le poid à vide doit être positif ou nul.\n{poids_vide = }")

    @property
    def capacite_max(self):
        return self._capacite_max

    @capacite_max.setter
    def capacite_max(self, capacite_max):
        self.check_capacite_max(capacite_max)
        self._capacite_max = capacite_max 

    def check_capacite_max(self, capacite_max):
        if not isinstance(capacite_max, float):
            raise TypeError(capacite_max)
        if capacite_max < 0:
            raise ValueError(f"La capacité maximale doit être positive ou nulle.\n{capacite_max = }")

    @property
    def niveau_remplissage(self):
        return self._niveau_remplissage

    @niveau_remplissage.setter
    def niveau_remplissage(self, niveau_remplissage):
        self.check_niveau_remplissage(niveau_remplissage)
        self._niveau_remplissage = niveau_remplissage 

    def check_niveau_remplissage(self, niveau_remplissage):
        if not isinstance(niveau_remplissage, float):
            raise TypeError(niveau_remplissage)
        if (niveau_remplissage < 0) or (niveau_remplissage > self._capacite_max):
            raise ValueError(f"Le niveau de remplissage doit être comprise entre 0 et {self._capacite_max}.\n{niveau_remplissage = }")

    @property
    def masse_volumique(self):
        return self._masse_volumique

    @masse_volumique.setter
    def masse_volumique(self, masse_volumique):
        self.check_masse_volumique(masse_volumique)
        self._masse_volumique = masse_volumique

    def check_masse_volumique(self, masse_volumique):
        if not isinstance(masse_volumique, float):
            raise TypeError(masse_volumique)
        if masse_volumique < 0:
            raise ValueError(f"La masse volumique doit être positive ou nulle.\n{masse_volumique = }")

    def poids_total(self) -> float:
        return self.poids_vide + self.niveau_remplissage * self._masse_volumique
    
    def remplir_citerne(self, quantite_ajoutee) -> None:
        if (quantite_ajoutee < 0) or ((quantite_ajoutee + self._niveau_remplissage) > self._capacite_max):
            raise ValueError(f"La quantité supplémentaire doit être comprise entre 0 et {self._capacite_max - self._niveau_remplissage}.\n{quantite_ajoutee = }")
        self._niveau_remplissage += quantite_ajoutee
        WaterTank.POIDS_TOTAL += quantite_ajoutee * self._masse_volumique
        WaterTank.NIVEAU_REMPLISSAGE_TOTAL += quantite_ajoutee
    
    def vider_citerne(self, quantite_retiree) -> None:
        if (quantite_retiree < 0) or (quantite_retiree > self._niveau_remplissage):
            raise ValueError(f"La quantité demandé doit être comprise entre 0 et {self._niveau_remplissage}.\n{quantite_retiree = }")
        self._niveau_remplissage -= quantite_retiree
        WaterTank.POIDS_TOTAL -= quantite_retiree * self._masse_volumique
        WaterTank.NIVEAU_REMPLISSAGE_TOTAL -= quantite_retiree


def main():
    citerne1 = WaterTank(poids_vide=1_000.0, capacite_max=100.0, niveau_remplissage=20.0)
    citerne2 = WaterTank(poids_vide=2_000.0, capacite_max=200.0, niveau_remplissage=120.0)
    citerne1.remplir_citerne(40)
    print(f"{citerne1.niveau_remplissage = }")
    citerne1.vider_citerne(10)
    print(f"{citerne1.niveau_remplissage = }")
    print(f"{WaterTank.POIDS_TOTAL}")
    print(f"{WaterTank.CAPACITE_TOTAL}")
    print(f"{WaterTank.NIVEAU_REMPLISSAGE_TOTAL}")

if __name__ == "__main__":
    main()