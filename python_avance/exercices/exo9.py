class Address:
    def __init__(self, street, city):
        self.street = str(street)
        self.city = str(city)
    
    def show(self):
        print(self.street)
        print(self.city)

class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def show(self):
        print(self.name + ' - ' + self.email)

class Contact(Address, Person):
    def __init__(self, street, city, name, email):
        Address.__init__(self, street, city)
        Person.__init__(self, name, email)
    
    def show(self):
        Person.show(self)
        Address.show(self)

class Notebook:
    def __init__(self):
        self.list_contact: list[Contact] = []
    
    def add(self, name, email, street, city):
        self.list_contact.append(Contact(name=name, email=email, street=street, city=city))
    
    def show(self):
        for contact in self.list_contact:
            contact.show()

notes = Notebook()
notes.add('Alice', 'alice@example.com', 'Lv 24', 'Sthlm')
notes.show()