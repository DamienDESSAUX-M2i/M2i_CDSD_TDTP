from typing import Callable


class ItemMenu():
    def __init__(
            self,
            signal: str,
            action: Callable,
            msg: str
            ):
        self.signal: str = signal
        self.action: Callable = action
        self.msg: str = msg


class Menu():
    def __init__(self):
        self.items_menu: list[ItemMenu] = []
        self.msg_menu = ""
    
    def add_item_menu(self, item_menu:ItemMenu) -> None:
        self.items_menu.append(item_menu)
        self.compute_msg_menu()
    
    def remove_item_menu(self, signal:str) -> None:
        for item_menu in self.items_menu:
            if item_menu.signal == signal:
                self.items_menu.pop(self.items_menu.index(item_menu))
                self.compute_msg_menu()
                break
    
    def compute_msg_menu(self) -> str:
        msg_menu = "=== Menu ===\n"
        for item_menu in self.items_menu:
            msg_menu += f"[{item_menu.signal}] {item_menu.msg}\n"
        msg_menu += "=> "
        self.msg_menu = msg_menu

    def show(self) -> None:
        while True:
            user_input: str = input(self.msg_menu)
            for item_menu in self.items_menu:
                if user_input in item_menu.signal:
                    item_menu.action()
                    break
            else:
                print("Erreur de saisie. Veuillez recommencer")