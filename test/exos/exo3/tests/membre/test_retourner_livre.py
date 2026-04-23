def test_retourner_livre_present_supprime_livre_et_retourne_true(membre, livre):
    membre.livres_empruntes.append(livre)

    result = membre.retourner_livre(livre)

    assert result is True
    assert livre not in membre.livres_empruntes


def test_retourner_livre_absent_retourne_false(membre, livre):
    result = membre.retourner_livre(livre)

    assert result is False
