def test_init_bibliotheque_nom_valide_attributs_initialises():
    from src.models import Bibliotheque

    biblio = Bibliotheque("Ma Bibliothèque")

    assert biblio.nom == "Ma Bibliothèque"
    assert biblio.livres == []
    assert biblio.membres == []
