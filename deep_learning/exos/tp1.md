# TP Pratique : MLP pour Classification binaire

## Contexte

Vous travaillez pour une entreprise de télécommunications. Vous devez développer un système intelligent pour détecter automatiquement les SMS spam et protéger les utilisateurs contre les messages indésirables (publicités, arnaques, phishing).

## Dataset

**SMS Spam Collection Dataset** (disponible sur Kaggle ou UCI ML Repository)

- ~5,500 SMS en anglais
- 2 classes : `spam` (13%) et `ham` (87%) - dataset déséquilibré!
- Exemples de SMS spam : "URGENT! You have won a $1000 prize! Call now!"
- Exemples de SMS ham : "Hey, are you free for dinner tonight?"

## Objectif d'apprentissage

Appliquer les concepts de demo01 sur des **données textuelles** :

- Transformation du texte en features numériques
- Gestion d'un dataset déséquilibré
- Construction d'un MLP pour classification binaire

---

## Tâches

### Tâche 1 : Chargement et Exploration du Dataset

**Ce que vous devez faire :**

1. **Téléchargez le dataset** :

   ```python
   import pandas as pd
   url = "https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv"
   df = pd.read_csv(url, sep='\t', names=['label', 'message'])
   ```

2. **Explorez les données** :
   - Affichez les 10 premières lignes avec `df.head(10)`
   - Calculez la distribution des classes : `df['label'].value_counts()`
   - Calculez le pourcentage de spam vs ham
   - Mesurez la longueur moyenne des SMS (nombre de caractères) par classe

3. **Visualisez des exemples** :
   - Affichez 5 exemples de spam
   - Affichez 5 exemples de ham
   - Créez un graphique de distribution de la longueur des messages

4. **Analysez le déséquilibre**

### Tâche 2 : Préparation des Données Textuelles

**Ce que vous devez faire :**

1. **Nettoyage du texte** (optionnel mais recommandé) :
2. **Encodage des labels** :
3. **Vectorisation du texte** avec **TF-IDF** (Term Frequency-Inverse Document Frequency)
4. **Split train/test** : avec scikit-learn
5. **One-hot encoding des labels** pour Keras :

### Tâche 3 : Construction du MLP pour Classification Binaire

**Ce que vous devez faire :**

1. **Construisez un MLP** adapté à la classification spam/ham :
2. **Compilez le modèle**

- **Input : 1000** (nombre de features TF-IDF)
- **Hidden layers : 64 → 32** (réduction progressive)
- **Dropout : 0.3, 0.2** (régularisation contre l'overfitting)
- **Output : 2 (softmax)** (spam ou ham)

### Tâche 4 : Entraînement avec Gestion du Déséquilibre

**Ce que vous devez faire :**

1. **Calculez les poids de classe** pour compenser le déséquilibre :

   ```python
   from sklearn.utils.class_weight import compute_class_weight
   import numpy as np

   # Calculer les poids pour équilibrer les classes
   class_weights = compute_class_weight(
       class_weight='balanced',
       classes=np.array([0, 1]),
       y=y_train
   )
   class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

   print(f"Poids des classes: {class_weight_dict}")
   # Exemple: {0: 0.57, 1: 3.85} → spam pèse ~7x plus lourd
   ```

2. **Entraînez le modèle** avec callbacks :

   ```python
   from tensorflow.keras.callbacks import EarlyStopping

   # Arrêt automatique si val_loss stagne
   early_stop = EarlyStopping(
       monitor='val_loss',
       patience=5,
       restore_best_weights=True
   )

   history = model.fit(
       # vos options...
       class_weight=class_weight_dict,  # ← Clé pour le déséquilibre!
   )
   ```

3. **Visualisez les courbes d'apprentissage** :

### Tâche 5 : Évaluation Détaillée

**Ce que vous devez faire :**

1. **Évaluez sur le test set**
2. **Calculez les métriques avancées** avec scikit-learn :
3. **Visualisez la matrice de confusion** :
4. **Analysez les erreurs**

**Métriques importantes :**

- **Accuracy** : % de prédictions correctes (peut être trompeur si dataset déséquilibré!)
- **Precision (spam)** : parmi les SMS prédits spam, combien sont vraiment spam ?
- **Recall (spam)** : parmi les vrais spam, combien avons-nous détectés ?
- **F1-score** : moyenne harmonique de precision/recall

### Tâche 6 : Tester le Modèle sur de Nouveaux SMS

**Ce que vous devez faire :**

1. **Créez une fonction de prédiction**

### Tâche 7 : Amélioration du Modèle (Bonus)

**Pistes d'amélioration :**

1. **Augmenter max_features du TF-IDF** :
   - Testez 2000, 3000 features au lieu de 1000

2. **Tester différentes architectures**

3. **Optimiser le seuil de décision** :
   - Au lieu de 0.5, testez 0.3 ou 0.7 pour la classification spam
