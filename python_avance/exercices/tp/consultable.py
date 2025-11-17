from abc import ABC, abstractmethod


class Consultable(ABC):
    @abstractmethod
    def consulter(self) -> None:
        raise NotImplementedError