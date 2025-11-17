def verification_adn(adn: str) -> bool:
    return set(adn).issubset({'a', 't', 'c', 'g'})

# Autre solution
def verification_adn2(adn: str) -> bool:
    for letter in adn:
        if letter not in "actg":
            return False
    return True

def saissie_adn(msg: str) -> str:
    adn: str = input(msg).lower()
    while not verification_adn(adn):
        adn = input(msg).lower()
        print("Erreur de saisie")
    return adn

# Autre solution
def saissie_adn2(question: str) -> str:
    while True:
        adn = input(question).lower()
        if verification_adn(adn):
            return adn
        print("Erreur de saisie")

def proportion(adn: str, sequence: str) -> int:
    return adn.count(sequence)

def main():
    adn = saissie_adn("Veuillez entrer une chaine ADN : ")
    sequence = saissie_adn("Veuillez entrer une séquence d'ADN : ")
    print(proportion(adn, sequence))

if __name__ == "__main__":
    main()