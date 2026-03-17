# Exercice 4 : Transfer Learning et Data Augmentation

## Objectif

Maîtriser le transfer learning avec des modèles pré-entraînés et optimiser les performances avec la data augmentation avancée.

## Contexte

Vous travaillez pour une startup de reconnaissance visuelle qui doit classifier des images de fleurs. Avec des données limitées (typique en production), vous devez utiliser le transfer learning et la data augmentation pour atteindre de bonnes performances.

## Dataset

**TF Flowers** (TensorFlow Datasets)

- **Source:** TensorFlow Datasets - `tf_flowers`
- **Installation:**
  ```python
  pip install tensorflow-datasets
  import tensorflow_datasets as tfds
  ds, info = tfds.load('tf_flowers', split=['train'], with_info=True, as_supervised=True)
  ```
- **Caractéristiques:**
  - ~3,670 images RGB de fleurs
  - 5 classes (daisy, dandelion, roses, sunflowers, tulips)
  - Images de tailles variables
  - Dataset léger et rapide à télécharger
  - Splits : train disponible

**Classes:**
- daisy (marguerite)
- dandelion (pissenlit)
- roses
- sunflowers (tournesols)
- tulips (tulipes)

## Tâches

### Tâche 1 : Chargement et Exploration

1. Chargez le dataset TF Flowers avec TensorFlow Datasets et divisez-le directement en 3 splits :
   ```python
   import tensorflow_datasets as tfds
   (train_ds, val_ds, test_ds), info = tfds.load(
       'tf_flowers',
       split=['train[:70%]', 'train[70%:85%]', 'train[85%:]'],
       with_info=True,
       as_supervised=True
   )
   ```
   - **train_ds** : 70% des données pour l'entraînement
   - **val_ds** : 15% pour la validation
   - **test_ds** : 15% pour le test final
   - `as_supervised=True` : retourne des tuples (image, label)
   - `with_info=True` : récupère les métadonnées (noms de classes, etc.)

2. Récupérez les informations du dataset :
   ```python
   num_classes = info.features['label'].num_classes
   class_names = info.features['label'].names
   ```

3. Analysez la distribution des classes sur le train set :
   - Comptez les images par classe avec une boucle
   - Visualisez avec un histogramme

4. Visualisez 20 images aléatoires avec leurs labels en utilisant `.take(20)`

5. Affichez les informations : nombre de classes, shape d'une image, nombre d'images par split

Attendus : Dataset chargé en 3 splits, visualisations claires

### Tâche 2 : Préparation des Datasets

1. Créez une fonction de prétraitement qui :
   - Redimensionne les images à 224x224 avec `tf.image.resize()`
   - Normalise les pixels entre 0 et 1 (division par 255.0)

2. Appliquez le prétraitement avec `.map()` et optimisez le pipeline :
   ```python
   train_ds_processed = train_ds.map(preprocess).cache().shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
   val_ds_processed = val_ds.map(preprocess).cache().batch(32).prefetch(tf.data.AUTOTUNE)
   test_ds_processed = test_ds.map(preprocess).cache().batch(32).prefetch(tf.data.AUTOTUNE)
   ```
   - `.cache()` : met en cache après le premier epoch
   - `.shuffle(1000)` : mélange 1000 images à la fois
   - `.batch(32)` : crée des batchs de 32 images
   - `.prefetch(AUTOTUNE)` : précharge les batchs en parallèle

3. Configurez la data augmentation avec `tf.keras.layers` :
   ```python
   data_augmentation = keras.Sequential([
       layers.RandomFlip("horizontal"),
       layers.RandomRotation(0.2),
       layers.RandomZoom(0.2),
       layers.RandomTranslation(0.2, 0.2)
   ])
   ```

Attendus : Datasets optimisés avec pipeline tf.data, data augmentation configurée

### Tâche 3 : Visualisation de l'Augmentation

1. Prenez une image d'exemple avec `next(iter(train_ds))[0]`
2. Redimensionnez-la à 224x224
3. Générez 19 variations augmentées avec `data_augmentation()`
4. Affichez l'image originale + 19 variations dans une grille 4x5
5. Vérifiez que les transformations sont visibles et réalistes

Attendus : Grille 4x5 avec original + 19 variations augmentées

### Tâche 4 : Transfer Learning - Feature Extraction (MobileNetV2)

1. Chargez **MobileNetV2** pré-entraîné sur ImageNet :
   - `weights='imagenet'`
   - `include_top=False`
   - `input_shape=(224, 224, 3)`
2. Gelez toutes les couches : `base_model.trainable = False`
3. Créez le modèle final avec `keras.Sequential` :
   - `data_augmentation` (appliquée dans le modèle)
   - `base_model` (MobileNetV2 gelé)
   - `GlobalAveragePooling2D()`
   - `Dense(128, activation='relu')`
   - `Dropout(0.3)`
   - `Dense(5, activation='softmax')`
4. Compilez avec Adam (lr=0.001), loss='sparse_categorical_crossentropy'
5. Entraînez 15 epochs avec `train_ds_processed` et `val_ds_processed`
6. Affichez les courbes accuracy et loss (train vs validation)

Attendus : Modèle MobileNetV2 entraîné avec data augmentation intégrée, courbes visualisées

### Tâche 5 : Comparaison de Modèles Pré-entraînés

1. Créez 2 autres modèles (feature extraction) :
   - **ResNet50**
   - **EfficientNetB0**
2. Entraînez chaque modèle 10 epochs (même config que MobileNetV2)
3. Comparez dans un tableau :
   - Validation accuracy
   - Nombre de paramètres
   - Vitesse d'inférence (ms/image sur 100 images)
4. Identifiez le meilleur modèle

Attendus : 3 modèles comparés, tableau pandas affiché

### Tâche 6 : Évaluation Finale sur Test Set

1. Évaluez le meilleur modèle sur le test set
2. Calculez les métriques :
   - Test accuracy
   - Test loss
3. Générez la confusion matrix
4. Affichez le classification report (precision, recall, F1 par classe)
5. Visualisez 20 prédictions (10 correctes + 10 erreurs)

Attendus : Évaluation complète, confusion matrix, visualisations

## Critères d'évaluation

- Dataset TF Flowers correctement chargé et divisé en 3 splits
- Pipeline tf.data optimisé (map, cache, shuffle, batch, prefetch)
- Data augmentation configurée avec tf.keras.layers
- Visualisations de l'augmentation claires
- MobileNetV2 implémenté en feature extraction avec augmentation intégrée
- 3 modèles comparés (MobileNetV2, ResNet50, EfficientNetB0)
- Tableau comparatif affiché
- Évaluation complète sur test set
- Confusion matrix et classification report générés

## Conseils

- Utilisez `tfds.load('tf_flowers', split=[...])` pour diviser directement le dataset
- Pas besoin de numpy : travaillez directement avec les datasets TensorFlow
- Utilisez `.map()` pour appliquer le prétraitement
- Intégrez `data_augmentation` dans le modèle Sequential
- N'oubliez pas `base_model.trainable = False` pour feature extraction
- `.cache()` et `.prefetch()` améliorent les performances
- Pour la vitesse d'inférence, mesurez sur un batch de test

## Ressources

- **TensorFlow Datasets:** https://www.tensorflow.org/datasets/catalog/tf_flowers
- **Transfer Learning Guide:** https://www.tensorflow.org/tutorials/images/transfer_learning
- **Data Augmentation:** https://www.tensorflow.org/tutorials/images/data_augmentation
- **MobileNetV2:** https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNetV2
