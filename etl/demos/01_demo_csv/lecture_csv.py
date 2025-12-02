import csv

# Lecture d'un fichier CSV
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # Lire l'en-tête
    headers = next(reader)
    print(f"Colonnes : {headers}")
    
    # Lire les données
    for row in reader:
        print(row)

# Lecture avec DictReader (plus pratique)
with open('data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        print(row)
        print(f"{row['nom']} - {row['age']} ans {row['ville']}")