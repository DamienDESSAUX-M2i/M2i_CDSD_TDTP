## Exercice 6: Configuration Avec Pydantic Settings

**Énoncé**:
Créez un modèle `Settings` pour configurer l'API:
- `app_name`: nom de l'app
- `debug`: mode debug (défaut False)
- `database_url`: URL de connexion à la base
- `secret_key`: clé secrète
- `api_v1_prefix`: préfixe des routes (défaut "/api/v1")

Chargez les valeurs depuis des variables d'environnement.

**Indices**:
- Héritez de `BaseSettings` (Pydantic v2) ou `Settings` (Pydantic v1)
- Utilisez `Field(..., env='VAR_NAME')` pour mapper les variables
- Créez une instance singleton au démarrage