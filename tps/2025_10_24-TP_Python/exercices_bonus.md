
## Exercice 1 : chapitres
1. Créer un programme qui permet d'afficher un nombre de chapitres et de sous-parties
2. Le programme demandera le nombre de chapitres ainsi que le nombre de sous-parties à afficher
```
Saisir un nombre de chapitres : 3
Saisir un nombre de sous-partie : 2
Chapitre 1
    Sous-partie 1.1
    Sous-partie 1.2
Chapitre 2
    Sous-partie 2.1
    Sous-partie 2.2
 Chapitre 3
    Sous-partie 3.1
    Sous-partie 3.2
```

## Exercice 2 : tables de multiplications
1. Créer un programme permettant d'afficher les tables de multiplications de 1 à 10
```
Table de 1
1 x 1 = 1
1 x 2 = 2
...
10 x 10 = 100
```

## Exercice 3 : population
1. L'accroissement de la population de Tourcoing est de 0.89%
2. En 2015 la ville comptait 96809 habitants
3. Combien d'années faut-il pour atteindre 120 000 habitants ?
4. Combien d'habitants y aura-t-il cette année-là ?
5. Écrire un programme permettant de résoudre ce problème

## Exercice 4 : sommes consécutives
1. Déclarer une variable nombre
2. À l'aide de boucles, afficher les suites de nombres qui permettent d'arriver au nombre inscrit précédemment
```
Saisir un nombre : 45
45 = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9
45 = 5 + 6 + 7 + 8 + 9 + 10
45 = 7 + 8 + 9 + 10 + 11
45 = 14 + 15 + 16
45 = 22 + 23
```


## Exercice 5 : nombres premiers
1. Un nombre premier est un nombre divisible par 1 et par soit-même uniquement
2. 1 n'est pas un nombre premier
3. Écrire un programme qui permet de savoir si un nombre est premier
```
Saisir un nombre ( > 1) : 3
3 est un nombre premier
```

## Exercice 6 : nombre mystère
1. Générer un nombre aléatoire entre 1 et 100
2. Faire saisir un nombre à l'utilisateur
3. Si le chiffre saisi est plus grand, écrire : Le nombre est plus petit
4. Si le chiffre saisi est plus petit, écrire : Le nombre est plus grand
5. Si le chiffre saisi est égal au chiffre aléatoire, écrire : Vous avez gagné en X tentatives
```
Saisir un nombre : 12
Le nombre est plus grand
Saisir un nombre : 14
Vous avez gagné en 2 tentative(s)
```

## Exercice 7 : factorielle
1. La factorielle d'un nombre positif est le quotient cumulatif des nombres allant de 1 à ce nombre
2. Exemple : la factorielle de 3 est 1 x 2 x 3 = 6
3. Réaliser un programme qui affiche la factorielle d'un nombre
```
Saisir un nombre : 5
5! = 1 x 2 x 3 x 4 x 5
Saisir un nombre : 2
2! = 1 x 2
```




## Exercice 8: pyramide

- Écrire un programme qui permet d'afficher un triangle isocèle formé d'étoiles \*.
- La hauteur du triangle (le nombre de lignes) sera saisie, comme dans l'exemple ci-contre.
- Il existe plusieurs méthodes pour arriver au résultat.
- Quelques pistes : f-strings, mathématiques, for imbriqués, incrémentation et décrémentation.

```
Saisir un nombre de ligne : 6

     *
    ***
   *****
  *******
 *********
***********
```



## Exercice 9 : 

- On dispose d'une feuille de papier d'épaisseur 0.1 mm.
- Combien de fois doit-on la plier au minimum pour que l'épaisseur dépasse 400m ?
- Écrire un programme en Python pour résoudre ce problème.
- Une fois fini, aborder le problème à l'inverse.
- Combien de fois doit-on déplier une feuille de 400m au minimum pour que l'épaisseur dépasse 0.1mm.



## Exercice 10:

- Réaliser un générateur des lettres de l'alphabet, soit en minuscules, soit en majuscules, en fonction d'un paramètre envoyé à sa création.
- Vous testerez ce générateur dans le cadre d'un programme de type console.



## Exercice 11:

- Écrire un programme permettant à un utilisateur de sauvegarder un texte secret dans un fichier.
- Si le fichier n'existe pas, il devra être créé avec un nouveau secret.
- L'utilisateur pourra :
  - Voir le secret
  - Modifier le secret
  - Quitter le programme (Cette action sauvegardera le fichier)
- Pour éviter tout problème, il est conseillé de ne lire et écrire le fichier qu'une seule fois à l'entrée et la sortie du programme.

## Exercice 12:

- Écrire un script qui demande les informations d'un produit :
  - Titre
  - Prix
  - Stock
- Il les ajoute ensuite dans un fichier produits.csv



## Exercice 13:

- Via l'utilisation d'une variable de type set contenant des noms de familles, vous devrez réaliser une application permettant à l'utilisateur :

  - de les stocker
  - de les afficher
  - de les éditer
  - de les supprimer

- Pour ce faire, l'utilisateur aura à sa disposition un menu permettant de naviguer entre les différentes fonctionnalités du programme, comme dans l'exemple ci-dessous.

```bash
=== MENU PRINCIPAL ===
1. Voir les noms de famille
2. Ajouter un nom de famille
3. Editer un nom de famille
4. Supprimer un nom de famille
0. Quitter le programme
Votre Choix : 1

=== LISTE NOMS DE FAMILLE ===
DUPONT
```


## Exercice 14:

- Réaliser une fonction qui permet, à partir d'une suite de nombres envoyés en paramètres, de retourner une chaîne de caractère correspondant à une syntaxe de ce type :
  - 1-2-3-4...-X
- Vous testerez cette fonction dans le cadre d'un programme de type console, après avoir récupéré ou généré une suite de nombres qui sera envoyée à votre fonction.



