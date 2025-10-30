class Ordinateur:
    def __init__(self, marque, nom, prix, quantite):
        self.marque = marque
        self.nom = nom
        self.prix = prix
        self.quantite = quantite

    def afficher(self):
        my_strs = []
        for varialbe, value in self.__dict__.items():
            my_strs.append(f"{varialbe} = {value}")
        return " | ".join(my_strs)

    def __str__(self):
        my_strs = [type(self).__name__]
        for varialbe, value in self.__dict__.items():
            my_strs.append(f"{varialbe} = {value}")
        return " | ".join(my_strs)
    
    def __len__(self):
        return self.quantite
    
    def __repr__(self):
        my_strs = [type(self).__name__]
        for _, value in self.__dict__.items():
            my_strs.append(f"{value}")
        return " ".join(my_strs)
    
    def __float__(self):
        return self.prix

    def __bool__(self):
        return self.quantite > 0
    
    def __add__(self, other: 'Ordinateur'):
        return self.prix + other.prix
    
    def __eq__(self, other: 'Ordinateur'):
        return (self.marque == other.marque) and (self.nom == other.nom)


ordinateur1 = Ordinateur("Dell", "Inspiron", 499.99, 5)
print(ordinateur1)
print(len(ordinateur1))
print(repr(ordinateur1))
print(float(ordinateur1))
print("J'ai du stock" if ordinateur1 else "Je n'ai pas de stock")
ordinateur2 = Ordinateur("MSI", "", 1199, 3)
print(ordinateur1 + ordinateur2)
ordinateur3 = Ordinateur("Dell", "Inspiron", 600, 2)
print(ordinateur1 == ordinateur3)