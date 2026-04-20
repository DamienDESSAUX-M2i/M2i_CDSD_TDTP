from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

SEED = 42
DIR_PATH = Path(__file__).parent.resolve()
DATA_PATH = DIR_PATH / "data" / "wine_data.csv"
MODEL_PATH = DIR_PATH / "models" / "model.pkl"

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# 1. Charge les données depuis `wine_data.csv`
df = pd.read_csv(DATA_PATH)

# 2. Sépare les features (X) et la target (y = quality)
target = "quality"
x = df.drop(columns=target)
y = df[target]

print(f"Features shape: {x.shape}")
print(f"Target shape: {y.shape}")

# 3. Divise en train/test (80/20)
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=SEED,
)

# 4. Entraîne un modèle RandomForest
model = RandomForestClassifier(random_state=SEED)
model.fit(x_train, y_train)

# 5. Affiche les métriques (accuracy, classification report)
y_pred = model.predict(x_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification report\n", classification_report(y_test, y_pred))

# 6. Sauvegarde le modèle dans `model.pkl`
joblib.dump(model, MODEL_PATH)
