# Exercice 1 : MLP pour la Classification

## Objectif
Construire et entraîner un perceptron multicouche (MLP) avec TensorFlow/Keras pour résoudre un problème de classification multiclasse.

## Contexte
Vous travaillez pour une startup de diagnostic médical. Vous devez classifier des images de chiffres manuscrits (MNIST) en utilisant un MLP. Cet exercice couvre les concepts fondamentaux : architecture, entraînement, évaluation.

## Dataset
Utilisez le dataset MNIST fourni par Keras :
- 60,000 images d'entraînement
- 10,000 images de test
- Classes : 0-9 (10 chiffres)
- Images : 28x28 pixels en niveaux de gris

## Tâches

### Tâche 1 : Chargement et Exploration
1. Chargez le dataset MNIST depuis `keras.datasets.mnist`
2. Explorez les dimensions : shape des images et labels
3. Affichez 10 images avec leurs labels
4. Analysez la distribution des classes
5. Vérifiez les valeurs des pixels (0-255)

Attendus : Dataset compris, visualisations claires

### Tâche 2 : Préparation des Données
1. Normalisez les pixels dans [0, 1]
2. Aplatissez les images 28x28 en vecteurs 784D
3. Convertissez les labels en one-hot encoding
4. Divisez en train/val/test (60k / 10k test)
5. Vérifiez les dimensions finales

Attendus : Données normalisées et formatées correctement

### Tâche 3 : Architecture MLP
1. Construisez un modèle Sequential avec Keras :
   - Input : 784 unités
   - Hidden 1 : 128 unités, activation ReLU
   - Hidden 2 : 64 unités, activation ReLU
   - Hidden 3 : 32 unités, activation ReLU
   - Output : 10 unités, activation Softmax
2. Compilez avec :
   - Optimizer : Adam (learning_rate=0.001)
   - Loss : categorical_crossentropy
   - Metrics : accuracy
3. Affichez le résumé du modèle

Attendus : Architecture définie et compilée correctement

### Tâche 4 : Entraînement
1. Entraînez le modèle :
   - Batch size : 32
   - Epochs : 20
   - Validation split : 0.2
2. Utilisez les callbacks :
   - EarlyStopping (monitor='val_loss', patience=3)
   - ReduceLROnPlateau (si possible)
3. Sauvegardez l'historique d'entraînement

Attendus : Modèle entraîné sans erreurs, historique sauvegardé

### Tâche 5 : Évaluation sur le Test Set
1. Évaluez sur le test set :
   - Accuracy
   - Loss
2. Prédisez sur les 10 premiers images de test
3. Comparez prédictions vs labels réels
4. Affichez 5 exemples (image + prédiction + vraie label)

Attendus : Évaluation complète, visualisations

### Tâche 6 : Analyse des Courbes d'Apprentissage
1. Tracez la courbe train loss vs validation loss
2. Tracez la courbe train accuracy vs validation accuracy
3. Analysez le comportement :
   - Y a-t-il overfitting?
   - Quand le modèle converge-t-il?
4. Identifiez les epochs optimaux

Attendus : Graphiques clairs, analyse critique

### Tâche 7 : Amélioration avec Régularisation
1. Ajoutez de la régularisation au modèle original :
   - Dropout(0.3) après chaque couche hidden
   - L2 regularization (kernel_regularizer='l2')
2. Comparez avec le modèle sans régularisation :
   - Même epoch count
   - Même données
3. Analysez l'impact sur l'overfitting

Attendus : Modèle amélioré, comparaison quantifiée

## Critères d'évaluation

- Dataset correctement chargé et exploré
- Préparation des données complète et correcte
- Architecture MLP implémentée exactement
- Entraînement converge sans erreurs
- Évaluation précise sur test set
- Courbes d'apprentissage visualisées et analysées
- Régularisation implémentée et comparée

## Conseils

- Importez : `from tensorflow.keras.datasets import mnist`
- Utilisez `model.summary()` pour vérifier l'architecture
- `model.fit()` retourne un historique (dictionnaire)
- `model.evaluate()` sur données de test
- `model.predict()` pour les prédictions
- Matplotlib pour les visualisations

## Bonus (Optionnel)

- Testez d'autres architectures (couches plus larges/profondes)
- Implémentez une loss function personnalisée
- Utilisez optimiseurs alternatifs (SGD, RMSprop)
- Visualisez les poids appris (première couche)
- Explorez l'impact de la batch size
