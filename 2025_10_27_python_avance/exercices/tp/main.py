from livre import Livre
from magazine import Magazine
from genre import Genre
from gui.main_menu import MainMenu


def main() -> None:
    livre1: Livre = Livre(titre="titre1", annee_publication=2000, auteur="auteur1", nb_pages=100, genre=Genre.FANTASTIQUE)
    livre2: Livre = Livre.livre(titre="titre2", auteur="auteur2", genre=Genre.ROMAN)
    magazine1: Magazine = Magazine(titre="titre1", annee_publication=1000, numero=1)
    magazine2: Magazine = Magazine(titre="titre2", annee_publication=1500, numero=2)
    documents: list[Livre|Magazine] = [livre1, livre2, magazine1, magazine2]
    
    main_menu: MainMenu = MainMenu(documents=documents)
    main_menu.show()


if __name__ == "__main__":
    main()