# TP Python : Gestion d'une bibliothèque

Application console en Python qui simule la gestion d'une bilbiothèque.

## Cloner le repository

Pour cloner le repository, éxécuter la commande bash
```bash
git clone https://github.com/DamienDESSAUX-M2i/M2i_CDSD_TDTP/tree/main/2025_10_27_python_avance/exercices/tp
```

## Comment lancer l'application

Pour lancer l'application, placez vous dans le dossier tp nouvellement créé et éxécuter la commande bash :
```bash
python main.py
```

## Architecture

Le dossier `menu` est un package permettant la création de menu console.
Pour créer un menu console, importez la classe Menu et créez une classe héritant de Menu.
```python
from menu.menu import Menu


class MyMenu(Menu):
    def __init__(self)
        self.menu_name = "Nom du menu"
```
