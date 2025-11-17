from abc import ABC, abstractmethod

class MyAbstractClass(ABC):
    def __init__(self, var1):
        self._var1 = var1

    @property
    def var1(self):
        print("MyAbstractClass getter")
        return self._var1
    
    @var1.setter
    def var1(self, var1):
        print("MyAbstractClass setter")
        self._var1 = var1

    def my_method(self):
        print("MyAbstractClass method")

    @abstractmethod
    def my_abstract_method(self):
        print("MyAbstractClass abstract method")

    @classmethod
    @abstractmethod
    def my_abstract_class_method(self):
        print("MyAbstractClass abstract class method")
    
    @staticmethod
    @abstractmethod
    def my_abstract_static_method():
        print("MyAbstractClass abstract static method")
    
    @property
    @abstractmethod
    def my_abstract_property(self):
        print("MyAbstractClass abstract property")


class MyClass(MyAbstractClass):
    def __init__(self, var1, var2):
        super().__init__(var1)
        self._var2 = var2

    @property
    def var2(self):
        print("MyClass getter")
        return self._var2
    
    @var2.setter
    def var2(self, var2):
        print("MyClass setter")
        self._var2 = var2

    def my_abstract_method(self):
        print("MyClass method")
    
    @classmethod
    def my_abstract_class_method(cls):
        print("MyClass class method")
    
    @staticmethod
    def my_abstract_static_method():
        print("MyClass static method")
    
    @property
    def my_abstract_property(self):
        print("MyClass property")


my_class = MyClass("var1", "var2")
print("=== Attributs ===")
my_class.var1 = "VAR1"
print(f"{my_class.var1 = }")
my_class.var2 = "VAR2"
print(f"{my_class.var2 = }")
print("=== Method ===")
my_class.my_method()
my_class.my_abstract_method()
MyClass.my_abstract_class_method()
MyClass.my_abstract_static_method()
MyAbstractClass.my_abstract_static_method()
my_class.my_abstract_property
