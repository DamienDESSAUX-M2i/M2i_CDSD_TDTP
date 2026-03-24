## Exercice 4: Validation de Formulaire

**Énoncé**:
Créez une route `/register` qui accepte un POST avec les champs:
- `username` (2-20 caractères)
- `email` (format valide)
- `password` (minimum 8 caractères)
- `age` (18-100)

Retournez une liste d'erreurs si la validation échoue.

Exemple:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secure123", "age": 25}'
# {"message": "Registration successful", "user": {...}}

curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "j", "email": "invalid", "password": "short", "age": 15}'
# {"errors": ["username too short", "invalid email", "password too short", "age must be 18+"]}
```

