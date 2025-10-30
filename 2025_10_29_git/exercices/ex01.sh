git init # Créer un reposiroty local
git add file # Staged le fichier 'file'
git commit -m "First commit" # Commit le fichier 'file'. Le fichier 'file' devient Unmodified
code file # Ouvrir le fichier 'file' dans VSCode pour le modifier. Le fichier 'file' deveint Modified
git commit -am "Modification fichier 'file'" # Staged puis Commit le fichier 'file' qui devient Unmodified
git log --oneline # Afficher l'historique des commits