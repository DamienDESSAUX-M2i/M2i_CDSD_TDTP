## Exercice 7: Validation Conditionnelle

**Énoncé**:
Créez un modèle `Événement` avec:
- `type`: "online" ou "offline"
- `title`: titre (requis)
- `location`: obligatoire si type="offline", sinon facultatif
- `url`: obligatoire si type="online", sinon facultatif
- `max_participants`: entier (>= 1)

**Indices**:
- Utilisez `model_validator` pour la logique conditionnelle
- Accédez à `self.type` pour vérifier le type
- Levez `ValueError` si la validation échoue