# Sans boucle
def compter_lettre_a(str1: str) -> int:
    return str1.lower().count("a")

print(compter_lettre_a("Abracadabra !"))

# Avec boucle
def compter_lettre_b(str1: str) -> int:
    cpt = 0
    for letter in str1.lower():
        if letter == 'b':
            cpt += 1
    return cpt

print(compter_lettre_b("Abracadabra !"))

# Avec lambda
print((lambda x: x.lower().count("a"))("Abracadabra !"))