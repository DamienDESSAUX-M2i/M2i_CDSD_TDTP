# python3

print("Hello World !\n")

ma_variable: int = 8
print(f"{ma_variable = }\n{type(ma_variable) = }\n")

ma_variable: float = 8.2
print(f"{ma_variable = :.2f}\n{type(ma_variable) = }\n") # :.2f => deux décimales

ma_variable: str = "8.2"
print(f"{ma_variable = }\n{type(ma_variable) = }\n")

ma_variable: bool = True
print(f"{ma_variable = }\n{type(ma_variable) = }\n")

print(f"Comparaison : {2 < 5 = }")
print(f"Comparaison : {2 > 5 = }")
print(f"Comparaison : {2 == 5 = }")
print(f"Comparaison : {2 <= 5 = }")
print(f"Comparaison : {2 >= 5 = }")
print(f"Comparaison : {2 != 5 = }\n")

ma_variable: str = input("Saisir un nombre entier : ")
print(f"Vous avez saisi : {ma_variable}.\nLe type de ce que vous avez saisi est : {type(ma_variable)}.\n")

# Le cast d'une variable correspond au changement de type d'une variable
try:
    ma_variable: int = int(ma_variable)
    print(f"Cast de la variable 'ma_varaible' : {type(ma_variable) = }")
except:
    print("Le cast de la variable 'ma_variable' n'a pas fonctionné.")
finally:
    print("\n")