def test_get_livres_disponibles_livres_mixtes_retourne_seulement_disponibles(
    bibliotheque, livre, livre_indisponible
):
    bibliotheque.ajouter_livre(livre)
    bibliotheque.ajouter_livre(livre_indisponible)

    result = bibliotheque.get_livres_disponibles()

    assert livre in result
    assert livre_indisponible not in result
    assert len(result) == 1


def test_get_livres_disponibles_aucun_livre_retourne_liste_vide(bibliotheque):
    assert bibliotheque.get_livres_disponibles() == []
