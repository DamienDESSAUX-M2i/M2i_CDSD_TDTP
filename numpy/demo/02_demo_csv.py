import numpy as np

data = np.genfromtxt("./pays.csv", delimiter=",", skip_header=1, usecols=(1, 2))
print("data :\n", data)

valeur_2015 = data[:, 0].astype(int)
valeur_2020 = data[:, 1].astype(int)

print("Moyenne 2015 : ", valeur_2015.mean())
print("Moyenne 2020 : ", valeur_2020.mean())

augmentation = valeur_2020 - valeur_2015
print(augmentation)

nom_pays = np.genfromtxt(
    "./pays.csv", delimiter=",", skip_header=1, usecols=0, dtype=str
)
print("nom_pays :\n", nom_pays)

print("Pays avec la plus grande augmentatoin : ", nom_pays[np.argmax(augmentation)])
