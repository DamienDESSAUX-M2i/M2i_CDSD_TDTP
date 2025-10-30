import math
from math import pi as pie
from itertools import product


# Opérateurs arithmétiques
print(f"Division décimale : {5 / 3 = }")
print(f"Division euclidienne : {5 // 3 = }")
print(f"Module : {5 % 3 = }")
print(f"Puissance : {5 ** 3 = }")
print(f"Puissance avec pow : {pow(5,3) = }")
print(f"Puissance avec math.pow : {math.pow(5,3) = }")
print(f"{pie = }")

# Opérateurs logiques
generic_tuple_bool: tuple[bool] = (True, False)
cartesian_product: tuple[tuple[bool]] = product(generic_tuple_bool,generic_tuple_bool)
for tuple_bool in cartesian_product:
    A,B = tuple_bool
    print(((A & (not B)) | ((not A) & B)) == (A ^ B))