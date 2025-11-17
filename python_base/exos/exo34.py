def panne_moteur(my_list: list) -> None:
    my_list.append(my_list.pop(0))

def passe_en_tete(my_list: list) -> None:
    # my_list.insert(0, my_list.pop(1))
    my_list[0], my_list[1] = my_list[1], my_list[0]

def sauve_honneur(my_list: list) -> None:
    # my_list.insert(len(my_list)-2, my_list.pop(len(my_list)-1))
    my_list[-1], my_list[-2] = my_list[-2], my_list[-1]

def tir_blaster(my_list: list) -> str:
    return my_list.pop(0)

def retour_inattendu(my_list: list, module: str) -> None:
    my_list.append(module)

def main():
    tatooine = ['Module A', 'Module B', 'Module C']
    print(f"Départ : {tatooine}")
    panne_moteur(tatooine)
    print(f"Panne moteur : {tatooine}")
    passe_en_tete(tatooine)
    print(f"Passe en tête : {tatooine}")
    sauve_honneur(tatooine)
    print(f"Sauve honneur : {tatooine}")
    module_pop = tir_blaster(tatooine)
    print(f"Tir blaster : {tatooine}")
    retour_inattendu(tatooine, module_pop)
    print(f"Retour inattendu : {tatooine}")

if __name__ == "__main__":
    main()