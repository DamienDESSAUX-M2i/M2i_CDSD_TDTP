cpt = 0
notes = []
while cpt < 3:
    user_input = input("Saisir un note : ")
    try:
        note = float(user_input)
        if 0 <= note <=20:
            notes.append(note)
            cpt += 1
    except:
        print("Saisie incorrecte")
    finally:
        pass

print(len(notes))
for i, note in enumerate(notes, start=1):
    print(f"Note {i} : {note}")