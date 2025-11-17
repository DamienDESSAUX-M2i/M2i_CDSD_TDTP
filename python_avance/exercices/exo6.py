from abc import ABC, abstractmethod


class Vehicule(ABC):
    def __init__(self, nom: str, marque: str):
        self.nom = nom
        self.marque = marque
    
    def __str__(self):
        my_strs = [type(self).__name__]
        for a, b in self.__dict__.items():
            my_strs.append(f"{a} = {b}")
        return ", ".join(my_strs)
    

class Motorise(ABC):
    @abstractmethod
    def demarrer(self):
        print("Démarrer")


class Electrique(ABC):
    @abstractmethod
    def recharger(self):
        print("Rechercher")


class Volant(ABC):
    @abstractmethod
    def decoller(self):
        print("Décoller")
    
    @abstractmethod
    def atterrir(self):
        print("Décoller")


class Flottant(ABC):
    @abstractmethod
    def naviguer(self):
        print("Naviguer")


class Voiture(Vehicule, Motorise):
    def __init__(self, nom, marque):
        super().__init__(nom, marque)
    
    def demarrer(self):
        return super().demarrer()


class VoitureHybride(Vehicule, Motorise, Electrique):
    def __init__(self, nom, marque):
        super().__init__(nom, marque)
    
    def demarrer(self):
        return super().demarrer()
    
    def recharger(self):
        return super().recharger()


class Hydravion(Vehicule, Motorise, Volant, Flottant):
    def __init__(self, nom, marque):
        super().__init__(nom, marque)
    
    def demarrer(self):
        return super().demarrer()
    
    def decoller(self):
        return super().decoller()
    
    def atterrir(self):
        return super().atterrir()
    
    def naviguer(self):
        return super().naviguer()


voiture = Voiture(marque="Renault", nom="21")
print(voiture)
voiture.demarrer()

voiturehybride = VoitureHybride(marque="Toyota", nom="Yaris")
print(voiturehybride)
voiturehybride.demarrer()
voiturehybride.recharger()

hydravion = Hydravion(marque="Waco", nom="YMF-5")
print(hydravion)
hydravion.demarrer()
hydravion.decoller()
hydravion.atterrir()
hydravion.naviguer()