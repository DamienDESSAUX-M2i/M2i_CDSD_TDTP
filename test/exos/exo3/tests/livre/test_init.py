def test_init_livre_parametres_valides_attributs_correctement_initialises():
    from src.models import Livre

    livre = Livre("1984", "Orwell", "123")

    assert livre.titre == "1984"
    assert livre.auteur == "Orwell"
    assert livre.isbn == "123"
    assert livre.disponible is True


def test_init_livre_disponibilite_false_attribut_correctement_initialise():
    from src.models import Livre

    livre = Livre("1984", "Orwell", "123", disponible=False)

    assert livre.disponible is False
