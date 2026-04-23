def test_trouver_livre_par_isbn_existant_retourne_livre(bibliotheque, livre):
    bibliotheque.ajouter_livre(livre)

    result = bibliotheque.trouver_livre_par_isbn("123")

    assert result == livre


def test_trouver_livre_par_isbn_inexistant_retourne_none(bibliotheque):
    assert bibliotheque.trouver_livre_par_isbn("999") is None
