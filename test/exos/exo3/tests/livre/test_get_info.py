def test_get_info_livre_valide_retourne_chaine_formatee(livre):
    result = livre.get_info()

    assert result == "1984 par Orwell (ISBN: 123)"
