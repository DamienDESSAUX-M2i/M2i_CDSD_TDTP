str1: str = "Text 1"
str2: str = "Text 2"
str3: str = "Text 3"

print(f"{str1 = }\n{str2 = }\n{str3 = }\n")
print(f"Concaténation : {str1 + str2 = }\n")

# methode .format
prenom: str = "Damien"
age: int = 31
# \n => retour chariot
# \t => tabulation
# \ => caractère d'échapement
print(f'Je m\'appelle\n\t{prenom}\net j\'ai\n\t{age} ans.\n')

my_str: str = "azerty"
print(f"{my_str.index("a") = }") # l'indice du caractère 'a'
print(f"{my_str[2] = }") # Le 3e caractère
print(f"{my_str[:3] = }") # 3 premiers caractères
print(f"{my_str[3:] = }") # du 4e caractère à la fin
print(f"{my_str[2:4] = }") # du 3e au 4e caractère
print(f"{my_str[0:6:2] = }") # avec un pas de 2
print(f"{my_str[-1] = }") # dernier caractère
print(f"{my_str[::-1] = }") # reverse
print(f"{my_str[:-4:-1] = }")