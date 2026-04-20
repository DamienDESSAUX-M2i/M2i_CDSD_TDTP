import os

name = os.getenv("NAME", "John Doe")
age = 0
try:
    age = int(os.getenv("AGE", "0"))
except:
    pass

if age > 18:
    print(f"Hello {name}, you can sign in")
else:
    print(f"Hello {name}, you are to young")
