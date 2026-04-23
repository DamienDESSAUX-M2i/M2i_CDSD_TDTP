def test_ajouter_membre_membre_valide_est_ajoute(bibliotheque, membre):
    bibliotheque.ajouter_membre(membre)

    assert membre in bibliotheque.membres
