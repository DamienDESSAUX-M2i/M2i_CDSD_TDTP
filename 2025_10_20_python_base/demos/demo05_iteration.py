# for
for i in range(5):
    print(f"Itération {i}")

# while
cpt = 0
while cpt < 5:
    print(f"{cpt = }")
    cpt += 1

# break / continue
for k in range(10):
    if k == 7:
        break
    if k == 4:
        continue
    print(f"{k = }")

# else
for n in range(3):
    pass
else:
    print("La boucle s'est terminée correctement")
for n in range(3):
    if n == 1:
        break
else:
    print("Ce message ne s'affiche pas")

# imbrication de boucles
from time import time

t0 = time()
for i in range(2):
    for j in range(3):
        print(f"{i}.{j}")
t1 = time()
print(f"execution time whit two for : {t1-t0}")

from itertools import product

t0 = time()
for i, j in product(range(2),range(3)):
    print(f"{i}.{j}")
t1 = time()
print(f"execution time whit itertools.product : {t1-t0}")
