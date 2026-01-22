import numpy as np

# np.ndarray
my_list = [1, 2, 3]

a = np.array(my_list)

print(a)
print(type(a))

print(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

print(np.arange(0, 10, 2))
print(np.zeros((2, 3)))
print(np.ones((3, 2)))
print(np.random.rand(3, 5))

# Indexing et slicing
arr = np.arange(10)
print("Tableau de base: ", arr)
print(f"{arr[1] = }")
print(f"{arr[2:5] = }")

mat = np.arange(1, 10).reshape(3, 3)
print("Matrice", mat)
print(f"{mat[1,2] = }")
print(f"{mat[:2,1:] = }")

# Arithmétique
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

print(f"{x+y = }")
print(f"{x*y = }")

# Statistiques
mat = np.arange(1, 10).reshape(3, 3)
print("Matrice", mat)
print("Somme de toutes les valeurs", mat.sum())
print("Somme horizontale", mat.sum(axis=1))
print("Somme verticale", mat.sum(axis=0))
print("Médiane", np.median(mat))
print("Médiane NaN exclus", np.nanmedian(mat))
print("Moyenne", mat.mean())
print("Ecart type", mat.std())
print("Min", mat.min())
print("Min position", mat.argmin())
print("Max", mat.max())
print("Max position", mat.argmax())
