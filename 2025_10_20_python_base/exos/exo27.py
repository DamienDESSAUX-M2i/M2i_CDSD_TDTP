def soustraction(a, b):
    print(f"Je soustrait {a} et {b}.")
    return a-b

print(f"{soustraction(2, 1) = }")

# lambda
soustraction_lambda = lambda a, b: print(f"Je soustrait {a} et {b} :") or (a - b)
print(soustraction_lambda(1, 1))