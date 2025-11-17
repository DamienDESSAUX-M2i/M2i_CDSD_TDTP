# Pour créer un tag sur le commit actuel
git tag v1.0

# Pour créer un tag avec un message
git tag -a v1.1 -m "nouvelle version stable"

# Lister les tags
git tag

# Afficher les détails d'un tag
git show v1.1

# Suppression d'un tag
git tag -d v1.1

# Se déplacer à l'aide des tags
git checkout v1.0

# Pousser les tags locaux sur le dépôt distant
git push origin --tags
git push --tags