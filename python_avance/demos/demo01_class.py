class MyClass:
    def __init__(self, value):
        self.my_attribute_public = value
        self._my_attribute_protected = value
        self.__my_attribute_private = value

    def my_method_public(self):
        return print(f"{self.my_attribute_public = }\n{self._my_attribute_protected = }\n{self.__my_attribute_private = }")

    def _my_method_protected(self):
        return print(f"{self.my_attribute_public = }\n{self._my_attribute_protected = }\n{self.__my_attribute_private = }")

    def __my_method_private(self):
        return print(f"{self.my_attribute_public = }\n{self._my_attribute_protected = }\n{self.__my_attribute_private = }")

    def __getattr__(self, name):
        if name == 'my_value':
            return self.my_attribute_public, self._my_attribute_protected, self.__my_attribute_private
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'my_value':
            self.my_attribute_public = value
            self._my_attribute_protected = value
            self.__my_attribute_private = value
        else:
            super().__setattr__(name, value)

    @property
    def my_attribute_protected(self):
        return self._my_attribute_protected

    @property
    def my_attribute_private(self):
        return self.__my_attribute_private

    @my_attribute_private.setter
    def my_attribute_private(self, value):
        self.__my_attribute_private = value

print("\n=== MyClass ===\n")
my_class: MyClass = MyClass(12)

print("\n=== method public / protégée / pvivée ===\n")
print(f"{my_class.my_method_public()}")
print(f"{my_class._my_method_protected()}")
# On ne peut pas utiliser une méthode privée
# print(f"{my_class.__my_method_private()}")

print("\n=== accés attributs public / protégé / privé ===\n")
print(f"{my_class.my_attribute_public = }")
print(f"{my_class._my_attribute_protected = }")
print(f"{my_class.my_attribute_protected = }")
# Message d'erreur que l'attribut est privé !
# print(f"{my_class.__my_attribute_private = }")
print(f"{my_class._MyClass__my_attribute_private = }")
print(f"{my_class.my_attribute_private = }")

print("\n=== modification attributs public / protégé / privé ===\n")
my_class.my_attribute_public = 24
print(f"{my_class.my_attribute_public = }")
my_class._my_attribute_protected = 24
print(f"{my_class.my_attribute_protected = }")
# On ne peut pas modifier un attribut privé directement
my_class.__my_attribute_private = 24
print(f"{my_class.my_attribute_private = }")
my_class._MyClass__my_attribute_private = 42
print(f"{my_class.my_attribute_private = }")
my_class.my_attribute_private = 24
print(f"{my_class.my_attribute_private = }")

print("\n=== __getattr__ et __setattr__ ===\n")
my_class.my_value = 56
print(f"{my_class.my_attribute_public = }")
print(f"{my_class.my_value = }")


class MySubClass(MyClass):
    def __init__(self, value):
        super().__init__(value)
    
    def other_method(self):
        return print(f"{self.my_attribute_public = }\n{self._my_attribute_protected = }\n'self.__my_attribute_private' ne peut pas être utilisé dans une sous classe")

print("\n=== MySubClass ===\n")
my_sub_class: MySubClass = MySubClass(24)


print("\n=== method public / protégée / pvivée ===\n")
print(f"{my_sub_class.my_method_public()}")
print(f"{my_sub_class._my_method_protected()}")
# On ne peut pas utiliser une méthode privée
# print(f"{my_sub_class.__my_method_private()}")
print(f"{my_sub_class.other_method()}")


print("\n=== accés attributs public / protégé / privé ===\n")
print(f"{my_sub_class.my_attribute_public = }")
print(f"{my_sub_class._my_attribute_protected = }")
print(f"{my_sub_class.my_attribute_protected = }")
# Message d'erreur que l'attribut est privé !
# print(f"{my_sub_class.__my_attribute_private = }")
print(f"{my_sub_class.my_attribute_private = }")

print("\n=== modification attributs public / protégé / privé ===\n")
my_sub_class.my_attribute_public = 24
print(f"{my_sub_class.my_attribute_public = }")
my_sub_class._my_attribute_protected = 24
print(f"{my_sub_class.my_attribute_protected = }")
# On ne peut pas modifier un attribut privé directement
my_sub_class.__my_attribute_private = 24
print(f"{my_sub_class.my_attribute_private = }")
my_sub_class._MyClass__my_attribute_private = 42
print(f"{my_sub_class.my_attribute_private = }")
my_sub_class.my_attribute_private = 24
print(f"{my_sub_class.my_attribute_private = }")

print("\n=== __getattr__ et __setattr__ ===\n")
my_sub_class.my_value = 87
print(f"{my_sub_class.my_value = }")