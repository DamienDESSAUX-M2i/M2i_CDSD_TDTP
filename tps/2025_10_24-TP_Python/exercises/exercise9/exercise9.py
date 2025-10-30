from math import log, ceil


def main() -> None:
    thickness_sheet: float = 0.1  # In millimeter
    thickness_sheets: float = 400  # In meter
    nb_folds: float = ceil(
        (log(thickness_sheets * 1_000) - log(thickness_sheet)) / log(2)
    )
    print(
        f"Pour obtenir un épaisseur de {thickness_sheets}m avec une feuille d'une épaisseur de {thickness_sheet}mm, on doit plier la feuille {nb_folds} fois seulement !"
    )


if __name__ == "__main__":
    main()
