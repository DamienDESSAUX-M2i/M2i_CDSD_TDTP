mois: int = 2
match mois:
    case m if m in [1, 3, 5, 7, 8, 10, 12]:
        print("31 jours dans le {mois}e mois")
    case m if m in [4, 6, 9, 11]:
        print("31 jours dans le {mois}e mois")
    case 2:
        print("28 ou 29 jours dans le {mois}e mois")
    case _:
        print(f"mois must be between 1 and 12")