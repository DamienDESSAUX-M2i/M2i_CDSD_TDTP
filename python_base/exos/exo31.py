def list_9(*args) -> any:
    if len(args) < 9:
        raise IndexError("Il nous faut au moins 9 éléments")
    return [x for x in args][8]

print(f"Le 9e élément de la liste est : {list_9(0,1,2,3,4,5,6,7,8,9)}")
print(list_9(1,2,3,4,5,6))