# Solution 1
for k in range(1, 101):
    match k:
        case k if k % 15 == 0:
            print("FizzBuzz")
        case k if k % 5 == 0:
            print("Buzz")
        case k if k % 3 == 0:
            print("Fizz")
        case _:
            print(f"{k}")

# Solution 2 'pythonesque'
for k in range(1, 101):
    output = ""
    if k % 3 == 0:
        output += "Fizz"
    if k % 5 == 0:
        output += "Buzz"
    # /!\ Si output est false, ie str vide,
    # regarde si k est true, ie différent de 0
    # Sinon affiche le contenu de output
    print(output or k)