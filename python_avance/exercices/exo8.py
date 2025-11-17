class Personne:
    def __init__(self, nom, prenom, no_telephone, mail):
        self.nom = nom
        self.prenom = prenom
        self.no_telephone = no_telephone
        self.mail = mail

    def __str__(self):
        my_strs = [type(self).__name__]
        for attribut, value in self.__dict__.items():
            my_strs.append(f"{attribut} = {value}")
        return " | ".join(my_strs)
    
class Travailleur(Personne):
    def __init__(self, nom, prenom, no_telephone, mail, nom_entreprise, adresse_entreprise, no_telephone_pro):
        super().__init__(nom, prenom, no_telephone, mail)
        self.nom_entreprise = nom_entreprise
        self.adresse_entreprise = adresse_entreprise
        self.no_telephone_pro = no_telephone_pro

class Scientifique(Travailleur):
    def __init__(self, nom, prenom, no_telephone, mail, nom_entreprise, adresse_entreprise, no_telephone_pro, disciplines, types_scientifique):
        super().__init__(nom, prenom, no_telephone, mail, nom_entreprise, adresse_entreprise, no_telephone_pro)
        self.disciplines = disciplines
        self.types_scientitique = types_scientifique

scientifique = Scientifique('Evarest', 'Galois', 3615, 'evarest.galois@univ.fr', 'Laboratoire mathématiques', "1 rue de l'université 80000 Lille", 0000000000, ['mathématiques'], ['Théorique'])
print(scientifique)