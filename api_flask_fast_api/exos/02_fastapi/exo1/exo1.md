## Exercice 1: Modèle Utilisateur Basique

**Énoncé**:
Créez un modèle Pydantic `User` avec:
- `id`: entier (non modifiable)
- `username`: chaîne (2-50 caractères)
- `email`: email valide
- `age`: entier optionnel (0-150 si fourni)
- `is_active`: booléen (par défaut True)

Testez avec une route POST `/users` qui accepte le modèle.