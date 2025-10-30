from menu import Menu, ItemMenu
import exercises
import random



def main():
    menu: Menu = Menu()
    item0: ItemMenu = ItemMenu(
        signal="0",
        action=exit,
        msg = "Quitter")
    menu.add_item_menu(item0)
    for a in exercises.__all__:
        print(a)
    item2: ItemMenu = ItemMenu(
        signal="2",
        action=exit,
        msg = "Afficher 'Hello World'"
        )
    menu.add_item_menu(item2)
    # menu.show()


if __name__ == "__main__":
    main()