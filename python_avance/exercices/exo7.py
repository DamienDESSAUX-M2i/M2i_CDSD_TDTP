class Electromenager():
    def allumer(self):
        print("allumer")

class Broyeur(Electromenager):
    def broyer(self):
        print("broyer")

class Mixeur(Broyeur):
    def mixer(self):
        print("mixer")

class Four(Electromenager):
    def cuire(self):
        print("cuire")

    def rechauffer(self):
        print("rechauffer")

class Cookeo(Mixeur, Four):
    pass

list_electromenager: list[Electromenager] = [Broyeur(), Mixeur(), Four(), Cookeo()]
for electromenager in list_electromenager:
    print(f"=== {type(electromenager).__name__} ===")
    electromenager.allumer()
    if "cuire" in dir(electromenager.__class__):
        electromenager.cuire()
    if "mixer" in dir(electromenager.__class__):
        electromenager.mixer()