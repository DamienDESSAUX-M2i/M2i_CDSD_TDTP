## Exercice 5: Réponses Typées Avec Génériques

**Énoncé**:
Créez une structure générique `ApiResponse<T>` qui enveloppe toute réponse:

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed",
  "timestamp": "2024-01-01T10:00:00"
}
```

Utilisez-la dans plusieurs routes.

**Indices**:
- Utilisez `Generic[T]` de `typing`
- Utilisez `datetime.now().isoformat()` pour les timestamps
- Spécialisez le modèle pour chaque réponse