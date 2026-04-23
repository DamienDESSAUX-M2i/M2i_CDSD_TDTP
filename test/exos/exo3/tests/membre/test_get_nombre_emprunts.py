def test_get_nombre_emprunts_aucun_livre_retourne_zero(membre):
    assert membre.get_nombre_emprunts() == 0


def test_get_nombre_emprunts_avec_livres_retourne_bon_nombre(membre, livre):
    membre.livres_empruntes.append(livre)

    assert membre.get_nombre_emprunts() == 1
