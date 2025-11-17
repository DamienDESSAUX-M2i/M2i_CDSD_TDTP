def print_name_age(name:str, age:int) -> None:
    """Print the age and the name of a user.

    Args:
        name (str): Name of a user.
        age (int): Age of a user.
    """
    print(f"{name} est agé(e) de {age} ans.")

def main() -> None:
    """Main function.
    """
    name: str = "damien".capitalize()
    age: int = 31
    print_name_age(name=name, age=age)


if __name__ == '__main__':
    main()