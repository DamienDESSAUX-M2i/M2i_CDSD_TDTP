# Exercice 04 :

```
bibliotheque/
│
├── src/
│   ├── __init__.py
│   ├── classes/
│   │   ├── __init__.py
│   │   ├── livre.py
│   │   ├── membre.py
│   │   └── bibliotheque.py
│   └── main.py
│
└── test/
    ├── __init__.py
    ├── test_livre.py
    ├── test_membre.py
    └── test_bibliotheque.py
```

## Livre

**Attributs :**

- `titre` (str)
- `auteur` (str)
- `isbn` (str)
- `disponible` (bool) - par défaut True

**Méthodes :**

- `emprunter()` : marque le livre comme non disponible, retourne True si succès, False si déjà emprunté
- `retourner()` : marque le livre comme disponible, retourne True si succès, False si déjà disponible
- `get_info()` : retourne une chaîne avec les infos du livre (format : "Titre par Auteur (ISBN: xxx)")

### Tests :

1. La création d'un livre avec tous ses attributs
2. Qu'un livre est disponible par défaut
3. L'emprunt d'un livre disponible
4. L'impossibilité d'emprunter un livre déjà emprunté
5. Le retour d'un livre emprunté
6. L'impossibilité de retourner un livre déjà disponible
7. La méthode `get_info()` retourne le bon format

---

## Membre

**Attributs :**

- `nom` (str)
- `prenom` (str)
- `numero_membre` (str)
- `livres_empruntes` (list) - liste vide par défaut
- `limite_emprunts` (int) - par défaut 3

**Méthodes :**

- `peut_emprunter()` : retourne True si le membre n'a pas atteint sa limite d'emprunts
- `emprunter_livre(livre)` : ajoute le livre à la liste si possible, retourne True/False
- `retourner_livre(livre)` : retire le livre de la liste, retourne True/False
- `get_nombre_emprunts()` : retourne le nombre de livres actuellement empruntés
- `get_nom_complet()` : retourne "Prénom Nom"

### Tests

**test création :**

1. Création d'un membre avec tous ses attributs
2. La liste de livres empruntés est vide par défaut
3. La limite d'emprunts est de 3 par défaut

**test emprunt :**

1. Un membre peut emprunter un livre
2. Le nombre d'emprunts augmente
3. Un membre ne peut pas emprunter plus de 3 livres
4. `peut_emprunter()` retourne False quand la limite est atteinte

**Test retour :**

1. Un membre peut retourner un livre emprunté
2. Le nombre d'emprunts diminue après un retour
3. On ne peut pas retourner un livre non emprunté

---

## Bibliotheque

**Attributs :**

- `nom` (str)
- `livres` (list) - liste de livres
- `membres` (list) - liste de membres

**Méthodes :**

- `ajouter_livre(livre)` : ajoute un livre au catalogue
- `ajouter_membre(membre)` : ajoute un membre
- `trouver_livre_par_isbn(isbn)` : retourne le livre ou None
- `trouver_membre_par_numero(numero)` : retourne le membre ou None
- `get_livres_disponibles()` : retourne la liste des livres disponibles

### Tests

**Test creation :**

1. Création d'une bibliothèque
2. Les listes de livres et membres sont vides au début

**Test gestion :**

1. Ajout de livres
2. Ajout de membres
3. Recherche de livre par ISBN
4. Recherche de membre par numéro
5. La liste des livres disponibles est correcte
