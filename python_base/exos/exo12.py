nb1, nb2, nb3 = 2, 5, 3

# Version 1
if nb1 > nb2:
    if nb1 > nb3:
        print(f"{nb1} est le maximum")
    else:
        print(f"{nb3} est le maximum")
else:
    if nb2 > nb3:
        print(f"{nb2} est le maximum")
    else:
        print(f"{nb3} est le maximum")

# Version 2 avec une variable supplémentarie
nbmax = nb1
if nb2 > nbmax:
    nbmax = nb2
if nb3 > nbmax:
    nbmax = nb3
print(f"{nbmax} est le maximum")