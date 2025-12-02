import csv

# Données à écrire : une liste de lignes (chaque ligne est une liste)
data = [
    ['nom', 'prenom', 'age', 'ville'],   # En-têtes
    ['Dupont', 'Jean', 35, 'Paris'],
    ['Martin', 'Marie', 28, 'Lyon'],
    ['Durant', 'Pierre', 42, 'Marseille']
]

# --- Écriture d'un CSV classique ---
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)       # Création du writer
    writer.writerows(data)          # Écrit toutes les lignes d'un coup

# --- Écriture avec DictWriter ---
with open('output2.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['nom', 'prenom', 'age', 'ville']   # Ordre des colonnes
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()            # Écrit la ligne d’en-tête automatiquement
    writer.writerow({               # Écrit une seule ligne en dict
        'nom': 'Dupont',
        'prenom': 'Jean',
        'age': 35,
        'ville': 'Paris'
    })
    writer.writerow({               # Écrit une seule ligne en dict
        'nom': 'Toto',
        'prenom': 'Tata',
        'age': 25,
        'ville': 'Lille'
    })
    writer.writerow({               # Écrit une seule ligne en dict
        'prenom': 'Tutu',
        'nom': 'Titi',
        'ville': 'Lille'
    })
    writer.writerows([{             
        'nom': 'Titi',
        'prenom': 'Tutu',
        'ville': 'Lille'
    },{              
        'nom': 'Titi',
        'prenom': 'Tutu',
        'ville': 'Lille'
    }])


    # - Si une clé manque dans le dictionnaire → la colonne sera vide (pas d'erreur)
    # - Si une clé en trop est présente → ValueError (la clé doit exister dans fieldnames)