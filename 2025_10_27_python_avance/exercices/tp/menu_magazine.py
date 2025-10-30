from menu.menu import Menu
from menu.item_menu import ItemMenu

from actions import Actions
from livre import Livre
from magazine import Magazine


class MenuMagazine(Menu):
    def __init__(self, documents: list[Livre|Magazine], parent: Menu):
        super().__init__()
        self.menu_name = "Menu Magazine"
        actions = Actions(documents)
        item_menu_consulter: ItemMenu = ItemMenu(signal="1", action=actions.consulter_document, msg="Consulter")
        self.add_item_menu(item_menu=item_menu_consulter)
        item_menu_quitter: ItemMenu = ItemMenu(signal="0", action=parent.show, msg="Retour")
        self.add_item_menu(item_menu=item_menu_quitter)