# Lister les branches (en local)
git branch

# Lister les branches (distantes)
git branch -r

# Créer une branche
git branch feature/login

# Créer une branche et s'y déplacer
git checkout -b feature/admin
git switch -c feature/class-livre

# Se déplacer sur la branche
git checkout feature/login
git switch feature/login

# Supprimer une branche
git branch -d feature/login