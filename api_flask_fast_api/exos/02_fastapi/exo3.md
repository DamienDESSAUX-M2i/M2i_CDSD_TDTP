## Exercice 3: Modèles Imbriqués

**Énoncé**:
Créez une structure pour un `Produit` contenant:
- `name`: nom du produit
- `price`: prix (> 0)
- `category`: catégorie (énumération: ELECTRONICS, CLOTHING, FOOD, OTHER)
- `stock`: entier (>= 0)
- `supplier`: objet Pydantic avec:
  - `name`: nom du fournisseur
  - `email`: email du fournisseur
  - `phone`: téléphone (optionnel)