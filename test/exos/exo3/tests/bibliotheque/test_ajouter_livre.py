def test_ajouter_livre_livre_valide_est_ajoute(bibliotheque, livre):
    bibliotheque.ajouter_livre(livre)

    assert livre in bibliotheque.livres
