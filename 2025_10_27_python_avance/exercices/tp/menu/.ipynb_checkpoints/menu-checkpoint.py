from menu.item_menu import ItemMenu
from exceptions import SignalException


class Menu:
    def __init__(self):
        self.items_menu: list[ItemMenu] = []
        self.menu_name: str = "Menu"
        self.msg_menu = ""
    
    def add_item_menu(self, item_menu:ItemMenu) -> None:
        self.items_menu.append(item_menu)
        self.compute_msg_menu()

    def compute_msg_menu(self) -> str:
        msgs_menu: list[str] = [f"=== {self.menu_name} ==="]
        for item_menu in self.items_menu:
            msgs_menu.append(f"[{item_menu.signal}] {item_menu.msg}")
        msgs_menu.append("=> ")
        self.msg_menu = "\n".join(msgs_menu)

    def user_input(self) -> ItemMenu:
        user_input: str = input(self.msg_menu)
        for item_menu in self.items_menu:
            if user_input in item_menu.signal:
                return item_menu
        raise SignalException("Erreur de saisie. Veuillez recommencer.")

    def show(self) -> None:
        while True:
            try:
                item_menu: ItemMenu = self.user_input()
                item_menu.action()
            except SignalException as e:
                e.display_message_error()