def test_peut_emprunter_sous_limite_retourne_true(membre):
    assert membre.peut_emprunter() is True


def test_peut_emprunter_limite_atteinte_retourne_false(membre_limite_atteinte):
    assert membre_limite_atteinte.peut_emprunter() is False
