class A:
    VARA0 = 0
    def __init__(self, varA1):
        self.varA1 = varA1
    
    @classmethod
    def methodA0(cls):
        print(f"{A.VARA0 = }")

    def methodA1(self):
        print(f"{self.varA1 = }")
    
    def methodA2(self):
        print("Polymorphisme")

class B(A):
    VARB0 = 1
    def __init__(self, varA1, varB1):
        super().__init__(varA1) # Constructeur de la class A
        self.varB1 = varB1
    
    @classmethod
    def methodB0(cls):
        print(f"{B.VARB0 = }")

    def methodB1(self):
        print(f"{self.varB1 = }")
        
    def methodA2(self):
        super().methodA2() # Appeller la méthode methodA2 de la classe A qui est override dans la classe B
        print("Override method")

b = B("varA1", "varB1")
print("=== class attribute ===")
print(f"{b.VARA0 = }")
print(f"{b.VARB0 = }")
print("=== attribute ===")
print(f"{b.varA1 = }")
print(f"{b.varB1 = }")
print("=== class method ===")
B.methodA0()
B.methodB0()
print("=== method ===")
b.methodA1()
b.methodA2()
b.methodB1()