from typing import TypedDict

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

# 1. Ajouter une nouvelle adresse à la liste.
def add_adress(addresses: list[Address], address: Address) -> None:
    addresses.append(address)

# 2. Éditer une adresse existante en modifiant ses informations.
def modify_adress(addresses: list[Address], index:int, numero: str = None, complement: str = None, intitule: str = None, commune: str = None, code_postal: str = None) -> None:
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
    
# 3. Supprimer une adresse de la liste.
def remove_adress(addresses: list[Address], index:int) -> None:
    addresses.pop(index)

# 4. Visualiser l'ensemble des addresses stockées.
def display_addresses(addresses: list[Address]) -> None:
    for i, address in enumerate(addresses, start=1):
        print(f"Adresse no{i}")
        print(f"Numéro de voie : {address["numero"]}")
        print(f"Complément : {address["complement"]}")
        print(f"Intitulée de voie : {address["intitule"]}")
        print(f"Commmune : {address["commune"]}")
        print(f"Code postal : {address["code_postal"]}")
        print("")

def user_address_imput(msg_code_postal: str, msg_commune: str, msg_complement: str, msg_intitule: str, msg_numero: str) -> Address:
    address: Address = {}
    address["numero"] = input(msg_numero)
    address["complement"] = input(msg_complement)
    address["intitule"] = input(msg_intitule)
    address["commune"] = input(msg_commune)
    address["code_postal"] = input(msg_code_postal)
    return address

def user_index_input(addresses: list[Address], msg_remove: str, msg_error: str) -> int:
    print(f"Le carnet d'adresses comprend {len(addresses)} adresses.")
    while True:
        user_input: str = input(msg_remove)
        try:
            index: int = int(user_input)
            if 1 <= index <= len(addresses):
                return index - 1
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)
        finally:
            pass

# Le programme doit permettre à l'utilisateur de choisir quelle action réaliser, et effectuer cette action sur les adresses stockées.
def menu(addresses: list[float], msgs: Msgs) -> None:
    msg_menu = msgs["msg_menu"]
    msg_error = msgs["msg_error"]
    msg_code_postal = msgs["msg_code_postal"]
    msg_commune = msgs["msg_commune"]
    msg_complement = msgs["msg_complement"]
    msg_intitule = msgs["msg_intitule"]
    msg_numero = msgs["msg_numero"]
    msg_remove = msgs["msg_remove"]

    while True:
        user_input = input(msg_menu).lower()
        match user_input:
            case "1":
                display_addresses(addresses=addresses)
            case "2":
                address: Address = user_address_imput(msg_code_postal=msg_code_postal, msg_commune=msg_commune, msg_complement=msg_complement, msg_intitule=msg_intitule, msg_numero=msg_numero)
                add_adress(addresses=addresses, address=address)
            case "3":
                index = user_index_input(addresses=addresses, msg_remove=msg_remove, msg_error=msg_error)
                remove_adress(addresses=addresses, index=index)
            case "4":
                menu_modify_address(addresses=addresses, msgs=msgs)
            case "stop":
                exit()
            case _:
                print(msg_error)

def menu_modify_address(addresses: list[Address], msgs: Msgs) -> None:
    msg_menu = msgs["msg_menu_modify_address"]
    msg_error = msgs["msg_error"]
    msg_modify = msgs["msg_modify"]
    msg_code_postal = msgs["msg_code_postal"]
    msg_commune = msgs["msg_commune"]
    msg_complement = msgs["msg_complement"]
    msg_intitule = msgs["msg_intitule"]
    msg_numero = msgs["msg_numero"]

    index = user_index_input(addresses=addresses, msg_remove=msg_modify, msg_error=msg_error)

    user_input = input(msg_menu)
    match user_input:
        case "1":
            modify_adress(addresses=addresses, index=index, numero=input(msg_numero))
        case "2":
            modify_adress(addresses=addresses, index=index, complement=input(msg_complement))
        case "3":
            modify_adress(addresses=addresses, index=index, intitule=input(msg_intitule))
        case "4":
            modify_adress(addresses=addresses, index=index, commune=input(msg_commune))
        case "5":
            modify_adress(addresses=addresses, index=index, code_postal=input(msg_code_postal))
        case _:
            print(msg_error)


def main() -> None:
    addresses: list[Address] = []
    msgs: Msgs = {}
    msgs["msg_menu"] = "[1] Pour afficher les adresses.\n[2] Pour ajouter une adresse.\n[3] Pour supprimer une adresse\n[4] Pour modifier une adresse\n[stop] pour quitter\nVotre choix : "
    msgs["msg_menu_modify_address"] = "[1] Numéro de voie\n[2] Complément d'adresse\n[3] Intitulée de voie\n[4] Nom de la commune\n[5] Code postal\nVotre choix : "
    msgs["msg_error"] = "Erreur de saisie."
    msgs["msg_commune"] = "Entrer le nom de la commune : "
    msgs["msg_code_postal"] = "Entrer le code postal : "
    msgs["msg_complement"] = "Entrer un complément d'adresse : "
    msgs["msg_numero"] = "Entrer le numéro de voie : "
    msgs["msg_intitule"] = "Entrer l'intitulé de la voie : "
    msgs["msg_remove"] = "Entrer l'indice de l'adresse à supprimer : "
    msgs["msg_modify"] = "Entrer l'indice de l'adresse à modifier : "

    menu(addresses=addresses, msgs=msgs)


if __name__ == "__main__":
    main()