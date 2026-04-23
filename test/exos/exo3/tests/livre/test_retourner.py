def test_retourner_livre_indisponible_retourne_true_et_devient_disponible(
    livre_indisponible,
):
    result = livre_indisponible.retourner()

    assert result is True
    assert livre_indisponible.disponible is True


def test_retourner_livre_deja_disponible_retourne_false(livre):
    result = livre.retourner()

    assert result is False
    assert livre.disponible is True
