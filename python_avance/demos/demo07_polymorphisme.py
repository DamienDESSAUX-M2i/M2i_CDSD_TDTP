class Chat:
    def miauler(self):
        print("Miaou")

class Chaton(Chat):
    # Override de la méthode miauler
    def miauler(self):
        print("Miaouuu")

class Chien:
    def miauler(self):
        print("Wouaf")

# Duck typing
## La méthode miauler est commune
list_animaux = (Chat(), Chien())
for animal in list_animaux:
    animal.miauler()