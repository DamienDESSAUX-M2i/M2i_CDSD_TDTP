from menu_console.item_menu import ItemMenu
from menu_console.exceptions import SignalException


class Menu:
    def __init__(self):
        self._items_menu: list[ItemMenu] = []
        self._menu_name: str = "Menu"
        self._menu_description: str = ""
        self._msg_menu = ""
    
    @property
    def items_menu(self) -> list[ItemMenu]:
        return self._items_menu
    
    @property
    def menu_name(self) -> str:
        return self._menu_name
    
    @menu_name.setter
    def menu_name(self, name: str) -> None:
        if type(name) is not str:
            raise TypeError("'menu_name' must be a sting.")
        self._menu_name = name

    @property
    def menu_description(self) -> str:
        return self._menu_description
    
    @menu_description.setter
    def menu_name(self, description: str) -> None:
        if type(description) is not str:
            raise TypeError("'menu_description' must be a sting.")
        self._menu_description = description

    def signal_exists(self, signal: str) -> bool:
        if type(signal) is not str:
            raise TypeError("'signal' must be a sting.")
        for item_menu in self._items_menu:
            if item_menu.signal == signal:
                return True
        return False

    def add_item_menu(self, item_menu:ItemMenu) -> None:
        if not isinstance(item_menu, ItemMenu):
            raise TypeError("'item_menu' must be an instance of ItemMenu.")
        if self.signal_exists(signal=item_menu.signal):
            raise SignalException("Two instances of ItemMenu must have different signals.")
        self._items_menu.append(item_menu)
        self.compute_msg_menu()

    def find_item_menu(self, signal: str) -> ItemMenu|None:
        if type(signal) is not str:
            raise TypeError("'signal' must be a sting.")
        for item_menu in self._items_menu:
            if item_menu.signal == signal:
                return ItemMenu
        return None

    def pop_item_menu(self, signal: str) -> ItemMenu:
        item_menu = self.find_item_menu(signal=signal)
        if item_menu is None:
            raise SignalException(f"No ItemMenu has the signal {signal}.")
        item_menu_pop = self._items_menu.pop(self._items_menu.index(item_menu))
        self.compute_msg_menu()
        return item_menu_pop

    def move_item_menu(self, item_menu: ItemMenu, step: int):
        raise NotImplementedError

    def compute_msg_menu(self) -> str:
        msgs_menu: list[str] = [f"=== {self._menu_name} ==="]
        if self._menu_description:
            msgs_menu.append(self._menu_description)
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