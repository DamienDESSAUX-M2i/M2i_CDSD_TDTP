nbmax = float(input("Donnez un nombre : "))
for k in range(5):
    nb = float(input("Donnez un nombre : "))
    if nb > nbmax:
        nbmax = nb
print(f"Le maximum est {nbmax}")