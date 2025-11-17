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
    msg_index_modify_addresses: str
    msg_modify_adresses: str
    msg_index_modify_persons: str
    msg_modify_persons: str
    msg_nom: str
    msg_prenom: str
    msg_date_naissance: str
    msg_add_person: str

class Person(TypedDict):
    nom: str
    prenom: str
    date_naissance: datetime.date

class Address(TypedDict):
    numero: str
    complement: str
    intitule: str
    commune: str
    code_postal: str
    membres_foyer: list[Person]

def display_addresses(addresses: list[Address]) -> None:
    for i, address in enumerate(addresses, start=1):
        print(f"Adresse no{i}")
        print(f"Numéro de voie : {address["numero"]}")
        print(f"Complément : {address["complement"]}")
        print(f"Intitulée de voie : {address["intitule"]}")
        print(f"Commmune : {address["commune"]}")
        print(f"Code postal : {address["code_postal"]}")
        for j, person in enumerate(address["membres_foyer"], strat=1):
            print(f"\tPersonne no{j}")
            print(f"\tNom : {person["nom"]}")
            print(f"\tPrénom : {person["prenom"]}")
            print(f"\tDate de naissance : {person["date_naissance"]}")
            print("")
        print("")

def user_index_input(
        my_list: list[Address],
        msg_index: str,
        msg_action: str,
        msg_error: str
        ) -> int:
    print(f"{msg_index}{len(my_list)}")
    while True:
        user_input: str = input(msg_action)
        try:
            index: int = int(user_input)
            if 1 <= index <= len(my_list):
                return index - 1
            else:
                print(msg_error)
        except ValueError:
            print(msg_error)
        finally:
            pass

def user_address_imput(msgs: Msgs) -> Address:
    address: Address = {}
    address["numero"] = input(msgs["msg_numero"])
    address["complement"] = input(msgs["msg_complement"])
    address["intitule"] = input(msgs["msg_intitule"])
    address["commune"] = input(msgs["msg_commune"])
    address["code_postal"] = input(msgs["msg_code_postal"])
    address["membres_foyer"] = user_person_imput(msgs=msgs)
    return address

def user_person_imput(msgs: Msgs) -> list[Person]:
    persons: list[Person] = []
    while True:
        user_input = input(msgs["msg_add_person"])
        match user_input:
            case "y":
                person: Person = {}
                person["nom"] = input(msgs["msg_nom"])
                person["prenom"] = input(msgs["msg_prenom"])
                person["date_naissance"] = input(msgs["msg_date_naissance"])
                persons.append(person)
            case 'n':
                break
            case _:
                print(msgs["msg_error"])
    return persons

def menu_addresses(addresses: list[Address], msgs: Msgs) -> None:
    while True:
        user_input = input(msgs["msg_menu"]).lower()
        match user_input:
            case "1":
                display_addresses(addresses=addresses)
            case "2":
                address: Address = user_address_imput(msgs=msgs)
                addresses.append(address)
            case "3":
                index: int = user_index_input(
                    my_list=addresses,
                    msg_index=msgs["msg_index_modify_adresses"],
                    msg_action=msgs["msg_modify_addresses"],
                    msg_error=msgs["msg_error"]
                    )
                addresses.pop(index)
            case "4":
                menu_modify_address(addresses=addresses, msgs=msgs)
            case "stop":
                exit()
            case _:
                print(msgs["msg_error"])

def menu_modify_address(addresses: list[Address], msgs: Msgs) -> None:
    index = user_index_input(
        my_list=addresses,
        msg_index=msgs["msg_index_modify_addresses"],
        msg_action=msgs["msg_modify_addresses"],
        msg_error=msgs["msg_error"]
        )
    user_input = input(msgs["msg_menu_modify_address"])
    match user_input:
        case "1":
            addresses[index]["numero"] = input(msgs["msg_numero"])
        case "2":
            addresses[index]["complement"] = input(msgs["msg_complement"])
        case "3":
            addresses[index]["intitule"] = input(msgs["msg_intitule"])
        case "4":
            addresses[index]["commune"] = input(msgs["msg_commune"])
        case "5":
            addresses[index]["code_postal"] = input(msgs["msg_code_postal"])
        case "6":
            menu_modify_person(persons=addresses[index]["membres_foyer"], msgs=msgs)
        case _:
            print(msgs["msg_error"])

# def menu_persons(persons: list[Person], msgs: Msgs) -> None:
#     while True:
#         user_input = input(msgs["msg_menu"]).lower()
#         match user_input:
#             case "1":
#                 display_addresses(persons=persons)
#             case "2":
#                 person: Address = user_address_imput(msgs=msgs)
#                 persons.append(address)
#             case "3":
#                 index: int = user_index_input(
#                     my_list=addresses,
#                     msg_index=msgs["msg_index_modify_adresses"],
#                     msg_action=msgs["msg_modify_addresses"],
#                     msg_error=msgs["msg_error"]
#                     )
#                 addresses.pop(index)
#             case "4":
#                 menu_modify_address(addresses=addresses, msgs=msgs)
#             case "stop":
#                 exit()
#             case _:
#                 print(msgs["msg_error"])

def menu_modify_person(persons: list[Person], msgs: Msgs):
    index = user_index_input(
        my_list=persons,
        msg_index=msgs["msg_index_modify_persons"],
        msg_action=msgs["msg_modify_persons"],
        msg_error=msgs["msg_error"]
        )
    user_input = input(msgs["msg_menu_modify_person"])
    match user_input:
        case "1":
            persons[index]["nom"] = input(msgs["msg_nom"])
        case "2":
            persons[index]["prenom"] = input(msgs["msg_prenom"])
        case "3":
            persons[index]["date_naissance"] = input(msgs["msg_date_naissance"])
        case "4":
            persons.pop(index)
        case _:
            print(msgs["msg_error"])

def main() -> None:
    addresses: list[Address] = []

    msgs: Msgs = {}
    msgs["msg_menu"] = "[1] Pour afficher les adresses.\n[2] Pour ajouter une adresse.\n[3] Pour supprimer une adresse\n[4] Pour modifier une adresse\n[stop] pour quitter\nVotre choix : "
    msgs["msg_menu_modify_address"] = "[1] Numéro de voie\n[2] Complément d'adresse\n[3] Intitulée de voie\n[4] Nom de la commune\n[5] Code postal\n[6] La liste des membres du foyer\nVotre choix : "
    msgs["msg_menu_modify_person"] = "[1] Nom\n[2] Prénom\n[3] Date de naissance\n[4] Supprimer le membre du foyer\nVotre choix : "
    msgs["msg_error"] = "Erreur de saisie."
    msgs["msg_commune"] = "Entrer le nom de la commune : "
    msgs["msg_code_postal"] = "Entrer le code postal : "
    msgs["msg_complement"] = "Entrer un complément d'adresse : "
    msgs["msg_numero"] = "Entrer le numéro de voie : "
    msgs["msg_intitule"] = "Entrer l'intitulé de la voie : "
    msgs["msg_remove"] = "Entrer l'indice de l'adresse à supprimer : "
    msgs["msg_index_modify_addresses"] = "Nombre d'adresses saisies : "
    msgs["msg_modify_addresses"] = "Entrer l'indice de l'adresse à modifier : "
    msgs["msg_index_modify_persons"] = "Nombre de personnes saisies : "
    msgs["msg_modify_persons"] = "Entrer l'indice de la personne à modifier : "
    msgs["msg_nom"] = "Entrer le nom : "
    msgs["msg_prenom"] = "Entrer le prénom : "
    msgs["msg_date_naissance"] = "Entrer la date de naissance : "
    msgs["msg_add_person"] = "Voulez vous ajouter un membre au foyer ? (y/n) : "

    menu_addresses(addresses=addresses, msgs=msgs)


if __name__ == "__main__":
    main()