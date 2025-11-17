class MyClassSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MyClassSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass(metaclass=MyClassSingleton):
    pass


my_class1 = MyClass()
print(id(my_class1))
my_class2 = MyClass()
print(id(my_class2))