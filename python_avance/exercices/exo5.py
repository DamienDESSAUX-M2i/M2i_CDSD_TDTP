from abc import ABC, abstractmethod
from math import pi


class Forme(ABC):
    def __init__(self, nom: str):
        self.check_nom(nom)
        self._nom = nom
    
    def check_nom(self, nom) -> None:
        if not isinstance(nom, str):
            raise TypeError(f"A name must be a string.\n{nom = }")
    
    def check_longueur(self, longueur) -> None:
        if not isinstance(longueur, (float, int)):
            raise TypeError(f"A length must be real number.\n{longueur = }")
        if longueur < 0:
            raise ValueError(f"A length must be positive or zero.\n{longueur = }")

    @property
    def nom(self) -> str:
        return self._nom
    
    @nom.setter
    def nom(self, nom) -> None:
        self.check_nom(nom)
        self._nom = nom
    
    @abstractmethod
    def calculer_aire(self) -> float|int:
        raise NotImplementedError
    
    @abstractmethod
    def calculer_perimeter(self) -> float|int:
        raise NotImplementedError
    
    def infos(self) -> str:
        return f"{self._nom}"


class Rectangle(Forme):
    def __init__(self, nom: str, longueur: float|int, largeur: float|int):
        super().__init__(nom)
        self.check_longueur(longueur=longueur)
        self._longueur = longueur
        self.check_longueur(longueur=largeur)
        self._largeur = largeur
    
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
    
    def calculer_aire(self) -> float|int:
        return self._longueur * self._largeur
    
    def calculer_perimeter(self) -> float|int:
        return (self._longueur + self._largeur)*2
    
    def infos(self) -> str:
        return f"{super().infos()} est un rectangle de longeur {self._longueur} cm et de largeur {self._largeur} cm."


class Cercle(Forme):
    def __init__(self, nom: str, rayon: float|int):
        super().__init__(nom)
        self.check_longueur(longueur=rayon)
        self._rayon = rayon
    
    @property
    def rayon(self) -> float|int:
        return self._rayon
    
    @rayon.setter
    def rayon(self, rayon) -> None:
        self.check_longueur(rayon)
        self._rayon = rayon
    
    def calculer_aire(self) -> float|int:
        return pi * self._rayon ** 2
    
    def calculer_perimeter(self) -> float|int:
        return 2 * pi * self._rayon
    
    def infos(self) -> str:
        return f"{super().infos()} est un cercle de rayon {self._rayon} cm."


def main():
    rectangle = Rectangle("ABCD", 12, 8)
    cercle = Cercle('C1', 6)
    print("=== Rectangle ===")
    print(f"{rectangle.infos() = }")
    print(f"{rectangle.calculer_aire() = }")
    print(f"{rectangle.calculer_perimeter() = }")
    print("=== Cercle ===")
    print(f"{cercle.infos() = }")
    print(f"{cercle.calculer_aire() = }")
    print(f"{cercle.calculer_perimeter() = }")


if __name__ == "__main__":
    main()