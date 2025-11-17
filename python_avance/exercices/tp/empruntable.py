from abc import ABC, abstractmethod


class Empruntable(ABC):
    def __init__(self, est_emprunte: bool):
        self.est_emprunte: bool = est_emprunte
    
    @abstractmethod
    def emprunter(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def rendre(self) -> None:
        raise NotImplementedError