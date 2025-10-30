from math import log, ceil


def main() -> None:
    nb_people_today: int = 96_809
    growth_rate: float = 0.89
    nb_people_tomorrow: int = 120_000
    nb_years: int = ceil(
        (log(nb_people_tomorrow) - log(nb_people_today)) / log(1 + growth_rate)
    )
    print(
        f"Avec un populaton de départ de {nb_people_today} habitants et un taux d'accroissement de {growth_rate * 100}%, il faudra {nb_years} année pour atteindre une population de {nb_people_tomorrow} habitants."
    )


if __name__ == "__main__":
    main()
