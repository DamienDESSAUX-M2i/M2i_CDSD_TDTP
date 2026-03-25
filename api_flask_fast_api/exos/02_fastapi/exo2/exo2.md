## Exercice 2: Validateurs Personnalisés

**Énoncé**:
Créez un modèle `Password` avec validation:
- `password`: au moins 8 caractères, doit contenir minuscule, majuscule, chiffre, symbole
- `confirm_password`: doit égaler `password`

Retournez des erreurs détaillées si la validation échoue.

Exemple:
```bash
# Valide
{"password": "SecurePass123!", "confirm_password": "SecurePass123!"}

# Invalide
{"password": "weak", "confirm_password": "weak"}
# Erreur: "password too short"
```
 