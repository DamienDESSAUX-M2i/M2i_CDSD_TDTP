def join_str(prenom: str, nom: str) -> str:
    """Join strings 'prenom' and 'nom' with one space.

    Args:
        prenom (str): Firstname.
        nom (str): Lastname.

    Raises:
        TypeError: Type of 'prenom' must be str.
        TypeError: Type of 'nom' must be str.

    Returns:
        str: Strings 'prenom' and 'nom' joined by a space.
    """
    if not isinstance(prenom, str):
        raise TypeError("The type of the argument 'prenom' must be str.")
    if not isinstance(nom, str):
        raise TypeError("The type of the argument 'nom' must be str.")
    
    return f"{prenom.capitalize()} {nom.capitalize()}"

def main() -> None:
    """Main function.
    """
    prenom: str = "damien"
    nom: str = "dessaux"
    print(join_str(nom=nom, prenom=prenom))

if __name__ == "__main__":
    main()