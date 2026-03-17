# Exercice 3 : CNN pour la Vision par Ordinateur

## Objectif
Construire et optimiser un réseau de convolution (CNN) pour la classification d'images CIFAR-10 avec données augmentées.

## Contexte
Vous développez un système de classification d'objets. Vous travaillez avec CIFAR-10 (voitures, chevaux, chats, etc.). Les données sont limitées, vous devez utiliser data augmentation et architecture CNN efficace.

## Dataset
CIFAR-10 depuis Keras :
- 50,000 images entraînement (32x32 RGB)
- 10,000 images test
- 10 classes : avion, automobile, oiseau, chat, cerf, chien, grenouille, cheval, bateau, camion

## Tâches

### Tâche 1 : Chargement et Exploration
1. Chargez CIFAR-10 depuis `keras.datasets.cifar10`
2. Visualisez 20 images aléatoires avec labels
3. Analysez les dimensions et range de pixels
4. Calculez la distribution de classes
5. Normalisez les pixels dans [0, 1]

Attendus : Dataset exploré et normalisé

### Tâche 2 : Architecture CNN Simple
1. Construisez un CNN :
   - Conv2D(32, 3x3, relu) + MaxPooling2D(2x2)
   - Conv2D(64, 3x3, relu) + MaxPooling2D(2x2)
   - Flatten
   - Dense(128, relu) + Dropout(0.3)
   - Dense(10, softmax)
2. Compilez avec Adam et categorical_crossentropy
3. Entraînez 15 epochs sans data augmentation

Attendus : Modèle entraîné, accuracy noté

### Tâche 3 : Data Augmentation
1. Implémentez ImageDataGenerator avec :
   - Rotation : 20 degrés
   - Width/height shift : 0.2
   - Horizontal flip
   - Zoom : 0.2
2. Entraînez le même CNN avec augmentation
3. Comparez les courbes avec/sans augmentation
4. Analysez l'impact sur train/val accuracy

Attendus : Comparaison quantifiée, visualisations

### Tâche 4 : CNN Profond
1. Construisez un CNN plus profond :
   - Conv2D(32, 3x3) × 2 + MaxPooling
   - Conv2D(64, 3x3) × 2 + MaxPooling
   - Conv2D(128, 3x3) × 2 + MaxPooling
   - Flatten + Dense(256) + Dropout(0.5)
   - Dense(128) + Dropout(0.3)
   - Dense(10, softmax)
2. Utilisez Batch Normalization après chaque Conv2D
3. Entraînez avec data augmentation
4. Comparez avec le modèle simple

Attendus : CNN profond entraîné, métriques comparées

### Tâche 5 : Évaluation Complète
1. Évaluez le meilleur modèle sur test set
2. Calculez accuracy, loss
3. Prédisez sur 20 images de test
4. Visualisez 10 prédictions (image + label + confiance)
5. Identifiez les erreurs (images mal classifiées)

Attendus : Évaluation précise, visualisations claires

### Tâche 6 : Optimisation d'Hyperparamètres
1. Testez différentes configurations :
   - Learning rates : 0.001, 0.0005, 0.0001
   - Batch sizes : 16, 32, 64
   - Dropout : 0.2, 0.3, 0.5
2. Comparez les performances
3. Identifiez la meilleure configuration
4. Justifiez vos choix

Attendus : Tuning systématique, résultats documentés

### Tâche 7 : Transfer Learning (Bonus)
1. Chargez un modèle pré-entraîné (MobileNetV2)
2. Gellez les premières couches (freeze)
3. Ajoutez des couches fully-connected pour CIFAR-10
4. Fine-tune sur CIFAR-10
5. Comparez avec CNN depuis zéro

Attendus : Transfer learning implémenté, performance améliorée

## Critères d'évaluation

- Dataset correctement exploré et augmenté
- Architecture CNN implémentée correctement
- Data augmentation intégrée et testée
- Batch normalization utilisée
- Évaluation précise et visualisée
- Hyperparamètres optimisés systématiquement
- Bonus transfer learning (optionnel)

## Conseils

- Utilisez `ImageDataGenerator` ou `image.ImageDataGenerator`
- `Conv2D`, `MaxPooling2D`, `BatchNormalization` de Keras
- Visualisez les images augmentées avec `plt.imshow()`
- Monitorez le rapport train/val loss pour l'overfitting
- Sauvegardez le meilleur modèle avec callbacks

## Bonus

- Implémentez une custom callback pour log les images prédites
- Visualisez les feature maps d'une couche Conv2D
- Testez MobileNetV2, EfficientNet pour transfer learning
- Implémentez mixup ou cutmix augmentation
- Créez une API simple pour tester le modèle
