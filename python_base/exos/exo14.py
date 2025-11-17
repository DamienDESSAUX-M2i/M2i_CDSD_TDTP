jour: int = 5
semaine: list[str] = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
match jour:
    case j if j in range(1,8):
        print(f"{semaine[j-1]} est le {jour}e de la semaine.")
    case _:
        print("'jour' must be between 1 and 7.")