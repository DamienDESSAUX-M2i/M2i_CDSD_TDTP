from functools import partialmethod
from typing import Callable

from menu_console.item_menu import ItemMenu
from menu_console.exceptions import SignalException


class Menu:
    """This class allows the creation and display of a console menu."""

    def __init__(self, menu_name: str = "Menu", menu_description: str = "", parent: 'Menu'= None) -> None:
        """Menu class constructor.

        Args:
            menu_name (str, optional): The name of the menu that will be displayed in the console. Defaults to "Menu".
            menu_description (str, optional): The description of the menu that will be displayed in the console. Defaults to "".
            parent (Menu, optional): The parent menu of the menu. Defaults to None.
        """
        self._items_menu: list[ItemMenu] = []
        self._menu_name: str = ""
        self.menu_name(menu_name)
        self._menu_description: str = ""
        self.menu_description(menu_description)
        self._msg_menu = ""
        self._parent: Menu = None
        self.parent(parent)
    
    @property
    def items_menu(self) -> list[ItemMenu]:
        """Getter of the attribute '_items_menu'.

        Returns:
            list[ItemMenu]: The list of menu items.
        """
        return self._items_menu
    
    @property
    def menu_name(self) -> str:
        """Getter of the attribute '_menu_name'.

        Returns:
            str: The name of the menu that will be displayed in the console.
        """
        return self._menu_name
    
    @menu_name.setter
    def menu_name(self, name: str) -> None:
        """Setter of the attribute '_menu_name'.

        Args:
            name (str): The name of the menu that will be displayed in the console.

        Raises:
            TypeError: 'menu_name' must be a string.
        """
        if type(name) is not str:
            raise TypeError("'menu_name' must be a string.")
        self._menu_name = name

    @property
    def menu_description(self) -> str:
        """Getter of the attribute '_menu_description'.

        Returns:
            str: The description of the menu that will be displayed in the console.
        """
        return self._menu_description
    
    @menu_description.setter
    def menu_description(self, description: str) -> None:
        """Setter of the attribute '_menu_description'.

        Args:
            description (str): The description of the menu that will be displayed in the console.

        Raises:
            TypeError: 'menu_description' must be a string.
        """
        if type(description) is not str:
            raise TypeError("'menu_description' must be a string.")
        self._menu_description = description

    @property
    def parent(self) -> 'Menu':
        """Getter of the attribute '_parent'.

        Returns:
            Menu: The parent of the menu that is an instance of the class Menu.
        """
        return self._parent
    
    @parent.setter
    def parent(self, parent: 'Menu'|None) -> None:
        """Setter of the attribute '_parent'.

        Args:
            parent (Menu | None): The parent of the menu.

        Raises:
            TypeError: 'parent' must be an instance of the class Menu.
        """
        if not ((isinstance(parent, 'Menu')) or (parent is not None)):
            raise TypeError("'parent' must be an instance of the class Menu.")
        self._parent = parent

    def signal_exists(self, signal: str) -> bool:
        """Checks if one of the menu items has the signal 'signal'.

        Args:
            signal (str): A signal of an menu item.

        Raises:
            TypeError: 'signal' must be a string.

        Returns:
            bool: Return 'True' if one of the menu items has the signal 'signal' and 'False' otherwise.
        """
        if type(signal) is not str:
            raise TypeError("'signal' must be a string.")
        for item_menu in self._items_menu:
            if item_menu.signal == signal:
                return True
        return False

    def add_item_menu(self, item_menu:ItemMenu) -> None:
        """Adds a menu item to the list of menu items.

        Args:
            item_menu (ItemMenu): A menu item to add.

        Raises:
            TypeError: 'item_menu' must be an instance of the class ItemMenu.
            SignalException: Two instances of ItemMenu must have different signals.
        """
        if not isinstance(item_menu, ItemMenu):
            raise TypeError("'item_menu' must be an instance of the class ItemMenu.")
        if self.signal_exists(signal=item_menu.signal):
            raise SignalException("Two instances of ItemMenu must have different signals.")
        self._items_menu.append(item_menu)
        self.compute_msg_menu()

    def find_item_menu(self, signal: str) -> ItemMenu|None:
        """Allows to get an item menu with his signal.

        Args:
            signal (str): The signal of an item menu.

        Raises:
            TypeError: 'signal' must be a string.

        Returns:
            ItemMenu|None: Return the item menu that has the signal 'signal or 'None' if no item menu has the signal 'signal'.
        """
        if type(signal) is not str:
            raise TypeError("'signal' must be a string.")
        for item_menu in self._items_menu:
            if item_menu.signal == signal:
                return ItemMenu
        return None

    def remove_item_menu(self, item_menu: ItemMenu) -> None:
        """Allows to remove an item menu.

        Args:
            item_menu (ItemMenu): The item menu to remove.

        Raises:
            TypeError: 'item_menu' must be an instance of the class ItemMenu.
            ValueError: 'item_menu' is not listed among the items menu.
        """
        if not isinstance(item_menu, ItemMenu):
            raise TypeError("'item_menu' must be an instance of the class ItemMenu.")
        if item_menu not in self._items_menu:
            raise ValueError("'item_menu' is not listed among the items menu.")
        self._items_menu.remove(item_menu)
        self.compute_msg_menu()

    def _move_item_menu_one_step(self, item_menu: ItemMenu, direction: str) -> None:
        if not isinstance(item_menu, ItemMenu):
            raise TypeError("'item_menu' must be an instance of ItemMenu.")
        if item_menu not in self._items_menu:
            raise ValueError(f"{item_menu = } is not listed among the menu items.")
        index_item_menu: int = self._items_menu.index(item_menu)
        match direction:
            case "up":
                if index_item_menu > 0:
                    self._items_menu.insert(index_item_menu - 1, self._items_menu.pop(index_item_menu))
            case "down":
                if index_item_menu < len(self._items_menu) - 1:
                    self._items_menu.insert(index_item_menu + 1, self._items_menu.pop(index_item_menu))
            case _:
                raise ValueError("'direction' must be 'up' or 'down'.")
        self.compute_msg_menu()

    move_up_item_menu = partialmethod(_move_item_menu_one_step, direction = "up")
    move_down_item_menu = partialmethod(_move_item_menu_one_step, direction = "down")

    def move_item_menu(self, item_menu: ItemMenu, step: int) -> None:
        if not isinstance(item_menu, ItemMenu):
            raise TypeError("'item_menu' must be an instance of ItemMenu.")
        if type(step) is not int:
            raise TypeError("'step' must be an integer.")
        move: Callable = self.move_up_item_menu if step >= 0 else self.move_down_item_menu
        for k in range(abs(step)):
            move(item_menu=item_menu)

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