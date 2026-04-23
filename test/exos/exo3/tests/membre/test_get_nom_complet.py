def test_get_nom_complet_membre_valide_retourne_nom_prenom(membre):
    result = membre.get_nom_complet()

    assert result == "John Doe"
