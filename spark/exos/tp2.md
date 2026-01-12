### Dataset Kaggle

**Superstore Sales Dataset**
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

### Partie 1 : Chargement et exploration

1. Charger le CSV en DataFrame avec l'option header
2. Afficher le schéma du DataFrame
3. Afficher les 20 premières lignes
4. Compter le nombre total de lignes
5. Afficher les régions uniques (colonne `Region`)

### Partie 2 : Transformations simples

1. Créer une colonne `Profit Margin` = `Profit` / `Sales`
2. Créer une colonne `Year` en extrayant l'année de `Order Date`
3. Créer une colonne `Total Value` = `Sales` - `Discount`
4. Afficher les 10 premières lignes avec ces nouvelles colonnes
5. **Mettre ce DataFrame en cache** (vous allez le réutiliser plusieurs fois)

### Partie 3 : UDF - Catégorisation des ventes

1. Créer une UDF `categorizeSale` qui prend le montant `Sales` et retourne :

   - "Petite vente" si < 100$
   - "Vente moyenne" si entre 100$ et 500$
   - "Grosse vente" si > 500$

2. Appliquer cette UDF pour créer une colonne `Sale Category`
3. Afficher quelques lignes avec cette nouvelle colonne
4. Compter le nombre de ventes par catégorie (Petite/Moyenne/Grosse)

### Partie 4 : UDF - Niveau de remise

1. Créer une UDF `discountLevel` qui prend `Discount` et retourne :

   - "Pas de remise" si = 0
   - "Remise faible" si entre 0 et 0.2
   - "Remise forte" si > 0.2

2. Appliquer cette UDF pour créer une colonne `Discount Level`
3. Calculer le CA total par niveau de remise

### Partie 5 : Agrégations basiques

1. Calculer le CA total (`Sales`) par région
2. Calculer le profit total par catégorie de produit (`Category`)
3. Calculer le nombre de commandes par segment client (`Segment`)
4. Identifier les 10 produits (`Product Name`) les plus vendus en quantité
5. Identifier les 5 états (`State`) avec le plus de CA

### Partie 6 : Broadcast Variable - Codes région

1. Créer une Map qui associe chaque région à un code :

```scala
val regionCodes = Map(
  "East" -> "EST",
  "West" -> "WST",
  "Central" -> "CTR",
  "South" -> "STH"
)
```

2. Broadcaster cette Map avec `spark.sparkContext.broadcast()`

3. Créer une UDF qui utilise cette broadcast variable pour créer une colonne `Region Code`

4. Afficher quelques lignes avec le code région

### Partie 7 : Broadcast Variable - Coefficients de priorité

1. Créer une Map de coefficients par catégorie :

```scala
val categoryPriority = Map(
  "Technology" -> 1.5,
  "Furniture" -> 1.2,
  "Office Supplies" -> 1.0
)
```

2. Broadcaster cette Map

3. Créer une UDF qui multiplie le `Profit` par le coefficient de sa catégorie pour créer une colonne `Weighted Profit`

4. Calculer le weighted profit total par catégorie
