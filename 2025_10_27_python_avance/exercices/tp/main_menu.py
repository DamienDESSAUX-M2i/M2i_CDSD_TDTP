from menu.menu import Menu
from menu.item_menu import ItemMenu

from livre import Livre
from magazine import Magazine
from menu_livre import MenuLivre
from menu_magazine import MenuMagazine


class MainMenu(Menu):
    def __init__(self, documents: list[Livre|Magazine]):
        super().__init__()
        self.menu_name = "Main Menu"
        menu_livre: MenuLivre = MenuLivre(documents=documents, parent=self)
        item_menu_livre: ItemMenu = ItemMenu(signal="1", action=menu_livre.show, msg="Livre")
        self.add_item_menu(item_menu=item_menu_livre)
        menu_magazine: MenuMagazine = MenuMagazine(documents=documents, parent=self)
        item_menu_magazine: ItemMenu = ItemMenu(signal="2", action=menu_magazine.show, msg="Magazine")
        self.add_item_menu(item_menu=item_menu_magazine)
        item_menu_quitter: ItemMenu = ItemMenu(signal="0", action=exit, msg="Quitter")
        self.add_item_menu(item_menu=item_menu_quitter)