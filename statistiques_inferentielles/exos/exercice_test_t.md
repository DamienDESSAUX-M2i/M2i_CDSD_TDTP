# Exercice : Test t de Student — CaféBoost

## Contexte

Tu travailles chez **CaféBoost**, une chaîne de cafés. Le directeur a 3 questions pour toi.

---

## Partie 1 : Test t à 1 échantillon

Le fournisseur de café affirme que ses sachets pèsent **250g** en moyenne.
Le directeur a des doutes. Tu pèses **15 sachets** au hasard :

```
248, 253, 246, 251, 249, 255, 247, 252, 250, 248,
254, 246, 251, 249, 253
```

### Questions

1. Calcule la moyenne et l'écart-type des poids.
2. Formule H₀ et H₁.
3. Vérifie la normalité des données (Shapiro-Wilk).
4. Réalise le test t à 1 échantillon. Le fournisseur dit-il la vérité ?

---

## Partie 2 : Test t pour 2 échantillons indépendants

CaféBoost teste **2 recettes** de cappuccino. On mesure la note de satisfaction (sur 10) donnée par des clients différents :

**Recette classique (12 clients) :**
```
7, 6, 8, 5, 7, 6, 7, 8, 6, 5, 7, 6
```

**Nouvelle recette (12 clients) :**
```
8, 9, 7, 8, 9, 8, 7, 9, 8, 9, 8, 7
```

### Questions

1. Calcule la moyenne de chaque groupe.
2. Formule H₀ et H₁.
3. Vérifie la normalité de chaque groupe (Shapiro-Wilk).
4. Vérifie l'homogénéité des variances (Levene).
5. Choisis et applique le bon test.
6. Calcule la taille d'effet (Cohen's d).
7. Rédige une conclusion pour le directeur.

---

## Partie 3 : Test t apparié

Le directeur envoie **10 baristas** en formation. On mesure le nombre de cafés préparés par heure **avant** et **après** la formation :

**Avant la formation :**
```
25, 28, 22, 30, 26, 24, 27, 23, 29, 25
```

**Après la formation :**
```
30, 33, 28, 34, 31, 29, 32, 28, 35, 30
```

### Questions

1. Calcule la différence (après - avant) pour chaque barista.
2. Calcule la moyenne des différences.
3. Formule H₀ et H₁.
4. Vérifie la normalité des différences.
5. Réalise le test t apparié.
6. La formation a-t-elle été efficace ?

---

## Consignes

- Tous les calculs en Python.
- Pour chaque test, suis le processus complet :
  1. Hypothèses (H₀ et H₁)
  2. Vérification des conditions (Shapiro, Levene)
  3. Choix du test
  4. Calcul et p-value
  5. Conclusion en français
- Seuil α = 0.05.
- Durée estimée : 45 minutes.
