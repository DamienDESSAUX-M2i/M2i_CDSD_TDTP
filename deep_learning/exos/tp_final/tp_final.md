# TP Final : Classification d'Aliments - Food-11

## Objectif

Construire un système complet de **classification d'aliments** sur le dataset **Food-11**, en appliquant **toutes les techniques** apprises pendant la formation :

- Exploration et préparation de données réelles
- Modélisation avancée (CNN custom, Transfer Learning, Ensemble)
- Optimisation complète (callbacks, hyperparameter tuning)
- Évaluation robuste (métriques, visualisations)
- Interprétabilité (Grad-CAM, feature maps)
- Déploiement (modèle production-ready)

---

## Dataset : Food-11

**Source :** Kaggle - [Food-11 Image Dataset](https://www.kaggle.com/datasets/trolukovich/food11-image-dataset)

**Téléchargement :**

1. Télécharger le dataset depuis Kaggle
2. Extraire dans `data/food-11/`

**Structure attendue :**

```
data/food-11/
├── training/
│   ├── 0/  (Bread)
│   ├── 1/  (Dairy product)
│   └── ...
├── validation/
└── evaluation/
```

**Caractéristiques :**

- **11 catégories d'aliments** : Bread, Dairy product, Dessert, Egg, Fried food, Meat, Noodles/Pasta, Rice, Seafood, Soup, Vegetable/Fruit
- **~9 866 images train** (variable par classe: 994-1500)
- **~3 430 images validation**
- **~3 347 images test/evaluation**
- Images **résolution variable** (typiquement 512x384)
- Images **réelles** issues du web

**Contexte réel :**
Vous développez une application mobile pour identifier automatiquement les plats photographiés par les utilisateurs :

- Tracking nutritionnel automatique
- Recommandations restaurant
- Partage social de repas
- Système temps réel (mobile deployment)

## Phases du TP Final

### Phase 1 : Exploration et Préparation

#### 1.1 Chargement et Inspection

**Tâches :**

1. Charger Food-11 depuis le dossier local avec `image_dataset_from_directory`
2. Inspecter :
   - Nombre d'images par classe (variable, ~900-1500 par classe en train)
   - Distribution des tailles d'images
   - Range des valeurs pixels
   - Qualité des images (résolution, netteté)

3. Analyse statistique :
   - Distribution des dimensions (height, width)
   - Distribution RGB (couleur dominante)
   - Aspect ratio moyen
   - Images corrompues ou manquantes?

4. Visualiser quelques exemples de chaque classe (11 classes)

#### 1.2 Stratégie de Préparation

**Décisions :**

1. **Taille cible** :
   - Option 1 : 224x224 (standard transfer learning)
   - Option 2 : 299x299 (InceptionV3, EfficientNet)
   - Option 3 : 384x384 (meilleure résolution, plus lent)

2. **Normalisation** :
   - ImageNet normalization (transfer learning)

3. **Data Augmentation** :
   - Rotation: ±15° (plats présentés à différents angles)
   - Zoom: ±20%
   - Brightness: ±15% (conditions d'éclairage variables)
   - Saturation: ±10% (qualité appareil photo)
   - Flip horizontal: activé

4. **Split validation** :
   - Créer validation set : 10% du train (7 575 images)
   - Train final : 68 175 images

### Phase 2 : Modélisation

#### 2.1 Architecture 1 : CNN Custom (Baseline)

**Objectif** : Établir une baseline avec CNN from scratch.

**Hyperparamètres :**

- Optimizer: Adam(lr=0.001)
- Batch size: 32
- Epochs: 50 (avec early stopping)
- Loss: sparse_categorical_crossentropy

#### 2.2 Architecture 2 : Transfer Learning - EfficientNetB0

**Objectif** : Utiliser un modèle pré-entraîné ImageNet.

Freeze base (10-15 epochs)

#### 2.3 Architecture 3 : Transfer Learning - EfficientNetB3

**Objectif** : Modèle plus profond pour meilleure performance.

#### 2.4 Architecture 4 : Ensemble (Bonus)

**Objectif** : Combiner plusieurs modèles pour boost performance.

### Phase 3 : Évaluation

#### 4.1 Métriques Globales

#### 4.2 Analyse des Erreurs

**Tâches :**

1. **Classes les plus faciles** (accuracy > 85%)

2. **Classes les plus difficiles** (accuracy < 60%)

3. **Matrice de confusion**

4. **Visualisation des erreurs** :
   - Afficher 20 images mal classifiées
   - Analyser pourquoi (occlusion, angle, similarité)

### Phase 5 : Interprétabilité

#### 5.1 Feature Maps Visualization

#### 5.2 GRAD-CAM

### Phase 6 : Déploiement

#### 6.1 Sauvegarde du Modèle

#### 6.2 Pipeline de Prédiction Réutilisable (Bonus)
