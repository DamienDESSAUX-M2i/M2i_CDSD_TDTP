# list
print("=== List ===")
my_list = [2, 1, 2] # création d'une liste
print(f"{my_list = }")
print(f"Elément d'index 0 : {my_list[0]}") # retourne l'élément d'index 0
my_list.sort() # trie
print(f"Sort : {my_list}")
my_list.append(3) # ajoute un élément à la fin
print(f"Append 3 : {my_list}")
my_list.insert(1, 2) # ajoute l'élément 2 à l'index 1
print(f"Insert 2 à l'index 1 : {my_list}")
my_list.extend([3, 1]) # fusionne les listes
print(f"Extend [3, 1] : {my_list}")
my_list.remove(2) # supprime tous les 2
print(f"Remove 2 : {my_list}")
elem_pop = my_list.pop(2) # supprimer et retourner l'élément d'index 2
print(f"Pop élément d'index 2 : {my_list}, {elem_pop}")
print(f"Count 1 : {my_list.count(1)}") # compte le nombre de 1

# lambda
print("\n=== Lambda ===")
print(f"{(lambda x, y: x + y)(1, 1) = }")
print(f"{(lambda x: x + 1)(5) = }")
my_list_str = ["python", "java", "c", "javescript"]
my_list_str_sorted = sorted(my_list_str, key=len) # trie selon la longueur de la chaine de caractère
print(f"{my_list_str_sorted}")
my_list_filter = list(filter(lambda x: x % 2 == 0, my_list)) # filtre les nombre pair
print(my_list_filter)
my_map = list(map(lambda x: x**2, my_list))
print(f"{my_map = }")

# tuple
print("\n=== tuple ===")
print(f"{type((1)) = }, {type((1,)) = }")
my_tuple = (2, 5, 3, 5)
print(f"{my_tuple = }")
print(f"Elément d'index 1 : {my_tuple[1]}")
print(f"Count 5 : {my_tuple.count(5)}")
print(f"Index 5 : {my_tuple.index(5)}")
v1, _, v2 = (1, "a", True)
print(f"Unpacking : {v1 = } et {v2 = }")
print(f"Fonction retour multiple : {(lambda x,y : (x+y, x*y))(1, 1) = }")

# set
print("\n=== Set ===")
my_set = {2, 5, 3, 5}
print(f"{my_set}")
my_set.add(4) # ajoute l'élément 4 et trie
print(f"Add 1 : {my_set}")
my_set.discard(3)
print(f"Discard 3 : {my_set}")
elem_pop = my_set.pop()
print(f"Pop 1er élément : {my_set}, {elem_pop}")
my_set.update({5, 7})
print(f"Update {5, 7} : {my_set}")
print(f"{my_set.issubset({1, 2, 3, 4, 5, 6, 7, 8, 9}) = }")
print(f"{my_set.issuperset({2, 5}) = }")
print(f"{my_set.isdisjoint({1, 2}) = }")
print(f"{my_set.union({1, 2, 5}) = }")
print(f"{my_set.intersection({1, 2, 5}) = }")
print(f"{my_set.difference({1, 2, 5}) = }")
print(f"{my_set.symmetric_difference({1, 2, 5}) = }")

# dict
print("\n=== Dict ===")
my_dict = {"k1": "a", "k2": 1, "k3": False, "k4": {"k1": [0, 1]}}
print(f"{my_dict}")
print(f"Keys : {my_dict.keys() = }")
print(f"Values : {my_dict.values() = }")
print(f"Items : {my_dict.items() = }")
my_dict.update({"k2": 1.0, "k5": {1}})
print(f"Update : {my_dict}")
value_pop = my_dict.pop("k1")
print(f"Pop 'k1' : {my_dict}, {value_pop}")