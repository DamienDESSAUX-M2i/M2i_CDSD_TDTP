class Rectangle:
    def __init__(self, longueur: float|int, largeur: float|int):
        self.check_longueur(longueur=longueur)
        self._longueur = longueur
        self.check_longueur(longueur=largeur)
        self._largeur = largeur
    
    def check_longueur(self, longueur) -> None:
        if not isinstance(longueur, (float, int)):
            raise TypeError(f"A length must be real number.\n{longueur = }")
        if longueur < 0:
            raise ValueError(f"A length must be positive or zero.\n{longueur = }")

    @property
    def longueur(self) -> float|int:
        return self._longueur
    
    @longueur.setter
    def longueur(self, longueur) -> None:
        self.check_longueur(longueur)
        self._longueur = longueur

    @property
    def largeur(self) -> float|int:
        return self._largeur
    
    @largeur.setter
    def largeur(self, largeur) -> None:
        self.check_longueur(largeur)
        self._largeur = largeur

    @property
    def perimeter(self) -> float|int:
        return (self._longueur + self._largeur) * 2
    
    @property
    def area(self) -> float|int:
        return self._longueur * self._largeur
    
class Pave(Rectangle):
    def __init__(self, longueur: float|int, largeur: float|int, hauteur: float|int):
        super().__init__(longueur=longueur, largeur=largeur)
        self.check_longueur(hauteur)
        self._hauteur = hauteur
    
    @property
    def hauteur(self) -> float|int:
        return self._hauteur
    
    @hauteur.setter
    def hauteur(self, hauteur) -> None:
        self.check_longueur(hauteur)
        self._hauteur = hauteur

    @property
    def perimeter(self) -> float|int:
        return 4 * (self._longueur + self._largeur + self._hauteur)

    @property
    def area(self) -> float|int:
        return 2 * (self._largeur * self._longueur + self._largeur * self._hauteur + self._longueur * self._hauteur)

    @property
    def volume(self) -> float|int:
        return super().area * self._hauteur

def main():
    pave: Pave = Pave(15.0,10.0,5)
    print(f"{pave.perimeter = }")
    print(f"{pave.area = }")
    print(f"{pave.volume = }")

if __name__ == "__main__":
    main()