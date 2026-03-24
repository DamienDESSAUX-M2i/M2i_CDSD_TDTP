## Exercice 3: Gestion d'une Liste de Livres

**Énoncé**:
Créez une API simple pour gérer une liste de livres en mémoire.

Routes:
- `GET /books` - Retourner tous les livres
- `GET /books/<id>` - Retourner un livre par ID
- `POST /books` - Ajouter un nouveau livre

Exemple POST:
```bash
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "author": "Orwell", "year": 1949}'
```
