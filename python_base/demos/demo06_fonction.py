# Fonction
a: float = 1
def fct(nb1: float, nb2: int = 2, *args, **kargs):
    global a    # Pour utiliser une variable global dans une fonction
    output = a + nb1 + nb2
    return output

print(f"{fct(1.2) = }")
print(f"{fct(1.2, 4) = }")
print(f"{fct(1.2, 4, 100, 200) = }")
print(f"{fct(1.2, 4, 100, 200, nb=1000) = }")

# Générateur
def gen(n):
    for i in range(n):
        yield i
    
gen3 = gen(3)
print(next(gen3))
print(next(gen3))
print(next(gen3))

# Générateur compréhension
gen3 = (i for i in range(3))