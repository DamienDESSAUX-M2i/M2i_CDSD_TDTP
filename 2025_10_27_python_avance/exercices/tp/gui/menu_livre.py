from menu_console.menu import Menu
from menu_console.item_menu import ItemMenu

from actions import Actions
from livre import Livre
from magazine import Magazine


class MenuLivre(Menu):
    def __init__(self, documents: list[Livre|Magazine], parent: Menu):
        super().__init__()
        self.menu_name = "Menu Livre"
        self.menu_description = "Que souhaitez-vous faire ?"
        actions = Actions(documents)
        item_menu_consulter: ItemMenu = ItemMenu(signal="1", action=actions.consulter_document, msg="Consulter")
        self.add_item_menu(item_menu=item_menu_consulter)
        item_menu_emprunt: ItemMenu = ItemMenu(signal="2", action=actions.emprunter_livre, msg="Emprunter")
        self.add_item_menu(item_menu=item_menu_emprunt)
        item_menu_rendre: ItemMenu = ItemMenu(signal="3", action=actions.rendre_livre, msg="Rendre")
        self.add_item_menu(item_menu=item_menu_rendre)
        item_menu_quitter: ItemMenu = ItemMenu(signal="0", action=parent.show, msg="Retour")
        self.add_item_menu(item_menu=item_menu_quitter)