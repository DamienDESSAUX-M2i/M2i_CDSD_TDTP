import pytest
from src.models import Bibliotheque, Livre, Membre


@pytest.fixture
def livre():
    return Livre("1984", "Orwell", "123")


@pytest.fixture
def livre_indisponible():
    return Livre("1984", "Orwell", "123", disponible=False)


@pytest.fixture
def membre():
    return Membre("Doe", "John", 1)


@pytest.fixture
def membre_limite_atteinte():
    m = Membre("Doe", "John", 1, limite_emprunts=1)
    m.livres_empruntes.append(Livre("Test", "A", "999"))
    return m


@pytest.fixture
def bibliotheque():
    return Bibliotheque("Test")
