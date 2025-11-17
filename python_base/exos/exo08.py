class Carre:
    """Cette classe regroupe les caractéristiques d'un carré.
    """
    def __init__(self, c:float) -> None:
        """Constructeur.

        Args:
            c (float): Le côté d'un carré.
        """
        self.__c = None
        self.set_c(c)
    
    def get_c(self) -> float:
        """Get self.__c.

        Returns:
            float: Le côté du carré.
        """
        return self.__c
    
    def set_c(self, c:float) -> None:
        """Set self.__c.

        Args:
            c (float): Le côté du carré.

        Raises:
            TypeError: c must be a float.
            ValueError: c must be greater of équal to 0.
        """
        # Check type
        if not isinstance(c, float):
            raise TypeError("The argument 'c' must be a float.")
        # Check interval
        if c < 0:
            raise ValueError("c must be greater of équal to 0.")
        
        self.__c = c

    @property
    def c(self) -> float:
        """Get self.__c.

        Returns:
            float: Le côté du carré.
        """
        return self.get_c()

    @property
    def area(self) -> float:
        """Calcule l'aire d'un carré.

        Returns:
            float: L'aire d'un carré de côté c.
        """
        return self.__c**self.__c

    @property
    def perimeter(self) -> float:
        """Calcule le périmètre d'un carré.

        Returns:
            float: Le périmètre d'un carré de côté c.
        """
        return 4*self.__c

def main() -> None:
    """Main function.
    """
    carre: Carre = Carre(5.2)
    print(f"Le périmètre d'un carré de côté {carre.c} cm est P = {carre.perimeter} cm")
    print(f"L'aire d'un carré de côté {carre.c} cm est A = {carre.area} cm²")


if __name__ == "__main__":
    main()