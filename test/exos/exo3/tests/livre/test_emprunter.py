def test_emprunter_livre_disponible_retourne_true_et_devient_indisponible(livre):
    result = livre.emprunter()

    assert result is True
    assert livre.disponible is False


def test_emprunter_livre_indisponible_retourne_false(livre_indisponible):
    result = livre_indisponible.emprunter()

    assert result is False
    assert livre_indisponible.disponible is False
