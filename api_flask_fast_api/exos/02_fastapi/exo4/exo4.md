
## Exercice 4: Validation Avec Listes

**Énoncé**:
Créez un modèle `Commande` (Order) contenant:
- `order_id`: identifiant unique (généralement UUID)
- `customer_email`: email valide
- `items`: liste de produits avec:
  - `product_id`: entier
  - `quantity`: entier (>= 1)
  - `price`: float (> 0)
- `total`: float (calculé ou fourni)

Validez que la liste n'est pas vide.

**Indices**:
- Utilisez `List[ItemModel]` pour la liste
- Validez la longueur minimale: `min_length=1`
- Optionnel: calculez le total automatiquement