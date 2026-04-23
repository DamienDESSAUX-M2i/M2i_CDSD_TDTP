def test_init_membre_parametres_valides_attributs_correctement_initialises():
    from src.models import Membre

    membre = Membre("Doe", "John", 1)

    assert membre.nom == "Doe"
    assert membre.prenom == "John"
    assert membre.numero_membre == 1
    assert membre.limite_emprunts == 3
    assert membre.livres_empruntes == []


def test_init_membre_limite_personnalisee_attribut_correctement_initialise():
    from src.models import Membre

    membre = Membre("Doe", "John", 1, limite_emprunts=5)

    assert membre.limite_emprunts == 5
