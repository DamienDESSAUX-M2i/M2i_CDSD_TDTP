def addition(a, b):
    return a + b

# Lors de l'appel du module, ce print sera exécuté
print(__name__)
print(addition(2, 5))

def main():
    print(addition(3, 8))


# La fonction main est lancée uniquement si le module est le point d'entrée
if __name__ == "__main__":
    main()