def test_emprunter_livre_sous_limite_ajoute_livre_et_retourne_true(membre, livre):
    result = membre.emprunter_livre(livre)

    assert result is True
    assert livre in membre.livres_empruntes


def test_emprunter_livre_limite_atteinte_retourne_false(membre_limite_atteinte, livre):
    result = membre_limite_atteinte.emprunter_livre(livre)

    assert result is False
    assert livre not in membre_limite_atteinte.livres_empruntes
