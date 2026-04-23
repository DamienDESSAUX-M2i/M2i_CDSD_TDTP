def test_trouver_membre_par_numero_existant_retourne_membre(bibliotheque, membre):
    bibliotheque.ajouter_membre(membre)

    result = bibliotheque.trouver_membre_par_numero(1)

    assert result == membre


def test_trouver_membre_par_numero_inexistant_retourne_none(bibliotheque):
    assert bibliotheque.trouver_membre_par_numero(999) is None
