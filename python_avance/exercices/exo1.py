class Gateau():
    def __init__(
            self,
            nom_gateau: str,
            temps_cuisson: int,
            liste_ingedients: list[str],
            etapes_recette: list[str],
            nom_du_createur: str
            ) -> None:
        self.nom_gateau = nom_gateau
        self.temps_cuisson = temps_cuisson
        self.liste_ingredients = liste_ingedients
        self.etapes_recette = etapes_recette
        self.nom_du_createur = nom_du_createur
    
    def display_liste_ingredients(self) -> None:
        print("=== Liste des ingrédients ===")
        for ingredient in self.liste_ingredients:
            print(ingredient)

gateau = Gateau(
    nom_gateau="nom_gateau",
    temps_cuisson=1,
    liste_ingedients=["a", "b"],
    etapes_recette=["1", "2"],
    nom_du_createur="a"
    )
gateau.display_liste_ingredients()