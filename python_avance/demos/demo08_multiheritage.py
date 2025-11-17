class A:
    def __init__(self, a):
        self.a = a

class B(A):
    def __init__(self, a, b):
        super().__init__(a)
        self.b = b

class C(A):
    def __init__(self, a, c):
        super().__init__(a)
        self.c = c

class D(B, C):
    def __init__(self, a, b, c, d):
        # super() fait référence au premier parent de la listr mro, ici B
        # Pour utiliser le constructeur de C on utilise C.__init__
        C.__init__(self, a, c)
        self.d = d

# .mro() => ordre de parcours des classes parents
print(B.mro())
print(D.mro())

d = D(1,2,3,4)

