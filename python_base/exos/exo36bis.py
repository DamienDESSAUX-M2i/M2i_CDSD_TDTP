from typing import TypedDict
from datetime import datetime

class Msgs(TypedDict):
    msg_menu: str
    msg_menu_modify_address: str
    msg_error: str
    msg_code_postal: str
    msg_commune: str
    msg_complement: str
    msg_intitule: str
    msg_numero: str
    msg_remove: str
    msg_modify: str
    msg_nom: str
    msg_prenom: str
    msg_date_naissance: str

# Chaque adresse sera un dictionnaire contenant les informations suivantes :
# - 'numero' : le numéro de voie.
# - 'complement' : le complément d'adresse (facultatif).
# - 'intitule' : l'intitulé de la voie.
# - 'commune' : le nom de la commune.
# - 'code_postal' : le code postal.
class Address(TypedDict):
    numero: str
    complement: str
    intitule: str
    commune: str
    code_postal: str
    nom: str
    prenom: str
    date_naissance: datetime.date

# 1. Ajouter une nouvelle adresse à la liste.
def add_adress(addresses: list[Address], address: Address) -> None:
    addresses.append(address)

# 2. Éditer une adresse existante en modifiant ses informations.
def modify_adress(
        addresses: list[Address],
        index:int, numero: str = None,
        complement: str = None,
        intitule: str = None,
        commune: str = None,
        code_postal: str = None,
        nom: str = None,
        prenom: str = None,
        date_naissance: str = None
        ) -> None:
    if code_postal is not None:
        addresses[index]["code_postal"] = code_postal
    if commune is not None:
        addresses[index]["commune"] = commune
    if complement is not None:
        addresses[index]["complement"] = complement
    if intitule is not None:
        addresses[index]["intitule"] = intitule
    if numero is not None:
        addresses[index]["numero"] = numero
    if nom is not None:
        addresses[index]["nom"] = nom
    if prenom is not None:
        addresses[index]["prenom"] = prenom
    if date_naissance is not None:
        addresses[index]["date_naissance"] = date_naissance
    
# 3. Supprimer une adresse de la liste.
def remove_adress(addresses: list[Address], index:int) -> None:
    addresses.pop(index)

# 4. Visualiser l'ensemble des addresses stockées.
def display_addresses(addresses: list[Address]) -> None:
    for i, address in enumerate(addresses, start=1):
        print(f"Adresse no{i}")
        print(f"Nom : {address["code_postal"]}")
        print(f"Prénom : {address["code_postal"]}")
        print(f"Date de naissance : {address["code_postal"]}")
        print(f"Numéro de voie : {address["numero"]}")
        print(f"Complément : {address["complement"]}")
        print(f"Intitulée de voie : {address["intitule"]}")
        print(f"Commmune : {address["commune"]}")
        print(f"Code postal : {address["code_postal"]}")
        print("")

def user_address_imput(msgs: Msgs) -> Address:
    address: Address = {}
    address["numero"] = input(msgs["msg_numero"])
    address["complement"] = input(msgs["msg_complement"])
    address["intitule"] = input(msgs["msg_intitule"])
    address["commune"] = input(msgs["msg_commune"])
    address["code_postal"] = input(msgs["msg_code_postal"])
    address["nom"] = input(msgs["msg_nom"])
    address["prenom"] = input(msgs["msg_prenom"])
    address["date_naissance"] = input(msgs["msg_date_naissance"])
    return address

def user_index_input(addresses: list[Address], msgs: Msgs) -> int:
    print(f"Le carnet d'adresses comprend {len(addresses)} adresses.")
    while True:
        user_input: str = input(msgs["msg_remove"])
        try:
            index: int = int(user_input)
            if 1 <= index <= len(addresses):
                return index - 1
            else:
                print(msgs["msg_error"])
        except ValueError:
            print(msgs["msg_error"])
        finally:
            pass

# Le programme doit permettre à l'utilisateur de choisir quelle action réaliser, et effectuer cette action sur les adresses stockées.
def menu(addresses: list[float], msgs: Msgs) -> None:
    while True:
        user_input = input(msgs["msg_menu"]).lower()
        match user_input:
            case "1":
                display_addresses(addresses=addresses)
            case "2":
                address: Address = user_address_imput(msgs=msgs)
                add_adress(addresses=addresses, address=address)
            case "3":
                index: int = user_index_input(addresses=addresses, msgs=msgs)
                remove_adress(addresses=addresses, index=index)
            case "4":
                menu_modify_address(addresses=addresses, msgs=msgs)
            case "stop":
                exit()
            case _:
                print(msgs["msg_error"])

def menu_modify_address(addresses: list[Address], msgs: Msgs) -> None:
    index = user_index_input(addresses=addresses, msgs=msgs)
    user_input = input(msgs["msg_menu_modify_address"])
    match user_input:
        case "1":
            modify_adress(addresses=addresses, index=index, numero=input(msgs["msg_numero"]))
        case "2":
            modify_adress(addresses=addresses, index=index, complement=input(msgs["msg_complement"]))
        case "3":
            modify_adress(addresses=addresses, index=index, intitule=input(msgs["msg_intitule"]))
        case "4":
            modify_adress(addresses=addresses, index=index, commune=input(msgs["msg_commune"]))
        case "5":
            modify_adress(addresses=addresses, index=index, code_postal=input(msgs["msg_code_postal"]))
        case "6":
            modify_adress(addresses=addresses, index=index, nom=input(msgs["msg_nom"]))
        case "7":
            modify_adress(addresses=addresses, index=index, prenom=input(msgs["msg_prenom"]))
        case "8":
            modify_adress(addresses=addresses, index=index, date_naissance=input(msgs["msg_date_naissance"]))
        case _:
            print(msgs["msg_error"])


def main() -> None:
    addresses: list[Address] = []

    msgs: Msgs = {}
    msgs["msg_menu"] = "[1] Pour afficher les adresses.\n[2] Pour ajouter une adresse.\n[3] Pour supprimer une adresse\n[4] Pour modifier une adresse\n[stop] pour quitter\nVotre choix : "
    msgs["msg_menu_modify_address"] = "[1] Numéro de voie\n[2] Complément d'adresse\n[3] Intitulée de voie\n[4] Nom de la commune\n[5] Code postal\n[6] Nom\n[7] Prénom\n[8] Date de naissance\nVotre choix : "
    msgs["msg_error"] = "Erreur de saisie."
    msgs["msg_commune"] = "Entrer le nom de la commune : "
    msgs["msg_code_postal"] = "Entrer le code postal : "
    msgs["msg_complement"] = "Entrer un complément d'adresse : "
    msgs["msg_numero"] = "Entrer le numéro de voie : "
    msgs["msg_intitule"] = "Entrer l'intitulé de la voie : "
    msgs["msg_remove"] = "Entrer l'indice de l'adresse à supprimer : "
    msgs["msg_modify"] = "Entrer l'indice de l'adresse à modifier : "
    msgs["msg_nom"] = "Entrer le nom : "
    msgs["msg_prenom"] = "Entrer le prénom : "
    msgs["msg_date_naissance"] = "Entrer la date de naissance : "

    menu(addresses=addresses, msgs=msgs)


if __name__ == "__main__":
    main()