str1: str = "Ma CHAINE De CaRaCtÈrE"
print(f"En minuscule : {str1.lower() = }")

str1_list: list[str] = list(str1)
print(f"En list de caractères : {",".join(str1_list) = }")

str1_split: list[str] = str1.split(" ")
str1_split = [my_str.capitalize() for my_str in str1_split]
print(f"En list de mots capitalisés : {" ".join(str1_split) = }")

# Autre méthode
print(f"En list de mots capitalisés : {str1.title() = }")