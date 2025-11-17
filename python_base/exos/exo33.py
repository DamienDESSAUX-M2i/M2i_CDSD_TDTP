def enter_nb_notes() -> int | None:
    """Allow the user to enter the number of notes they wish to enter.

    Returns:
        int | None: Number of notes the user will enter.
    """
    nb_notes: int|None = 0

    while True:
        print("Saisir le nombre de notes à entrer\nou 'non' pour ne pas définir de nombre de notes.")
        user_input = input("Votre saisie : ").lower()
        if user_input == 'non':
            nb_notes = None
            break
        try:
            nb_notes = int(user_input)
            if nb_notes >= 0 :
                break
            else:
                print("Saisir un entier positif")
        except ValueError:
            print("Saisir un nombre entier")
        finally:
            pass
    
    return nb_notes

def enter_notes(nb_notes: int|None) -> list[float]:
    """Allow the user to enter notes.

    Args:
        nb_notes (int | None): Number of notes user will enter.

    Raises:
        TypeError: 'nb_notes' must be an int or None.

    Returns:
        list[float]: User-entered notes.
    """
    # check type
    if not (isinstance(nb_notes, int) or nb_notes is None):
        raise TypeError("The argument 'nb_notes' must be an int or None.")
    
    notes = []

    cpt_notes = 0
    while (nb_notes > 0) or (nb_notes is None):
        user_input = input("Saisir une note ou -1 pour arrêter la saisie : ")
        if user_input == "-1":
            break
        try:
            note = float(user_input)
            if 0 <= note <= 20:
                notes.append(note)
                cpt_notes += 1
                if cpt_notes == nb_notes:
                    break
            else:
                print("Saisir un nombre entre 0 et 20")
        except ValueError:
            print("Saisir un nombre")
        finally:
            pass
    
    return notes

def display_notes(notes: list[float]) -> None:
    """Display notes enter by user.

    Args:
        notes (list[float]): User-entered notes.

    Raises:
        TypeError: 'notes' must be a list[float].
    """
    # Check type
    if not (isinstance(notes, list) and all(type(note) is float for note in notes)):
        raise TypeError("The argument 'notes' must be list[int].")
    
    nb_notes = len(notes)
    while True:
        print("[1] Pour afficher la note minimal.")
        print("[2] Pour afficher la note maximal.")
        print("[3] Pour afficher la moyenne des notes.")
        print("[4] Pour quitter.")
        user_input = input("Votre choix : ").lower()
        match user_input:
            case "1":
                print(f"La note minimale est {min(notes)}" if nb_notes != 0 else "Pas de note")
            case "2":
                print(f"La note maximale est {max(notes)}" if nb_notes != 0 else "Pas de note.")
            case "3":
                print(f"La moyenne est {sum(notes)/nb_notes}" if nb_notes != 0 else "Pas de note")
            case "4":
                exit()
            case _:
                print("Saisie incorrecte")

def main():
    """Main function
    """
    nb_notes = enter_nb_notes()
    notes = enter_notes(nb_notes)
    display_notes(notes)


if __name__ == "__main__":
    main()