## Exercice 6: Blog Simple (CRUD Complet)

**Énoncé**:
Créez une API blog complète avec:
- `GET /posts` - Lister tous les articles
- `GET /posts/<id>` - Détail d'un article
- `POST /posts` - Créer un article
- `PUT /posts/<id>` - Modifier un article
- `DELETE /posts/<id>` - Supprimer un article

Structure d'un post:
```json
{
  "id": 1,
  "title": "Mon Premier Article",
  "content": "Contenu...",
  "author": "John",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

