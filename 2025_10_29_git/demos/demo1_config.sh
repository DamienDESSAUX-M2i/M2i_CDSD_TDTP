# Initialiser un dépot
git init # Ici, un dossier caché .git va se créer dans le dossier courant.

# Configuration utilisateur
git config --global user.name "Damien DESSAUX"
git config --global user.email "damien.dessaux@labom2iformation.fr" 

# Pour récupérer l'ensembles des éléments de configuration
git config --list
git config user.name 

# Permet de connaitre toutes les commandes disponibles sur git
git help

# Consulter de l'aide pour une commande
git help command
git config --help
git config -h

# Permet de définir la branche par défaut comme étant 'main' et non 'master'
git config --global init.defaultBranch main

# Créer des alias
git config --global alias.st status
git config --global alias.ck checkout
git config --global alias.br branch