# git status me permet d'afficher l'état actuelle de mes fichiers dans le dossier courant. 
git status

echo "mon premier fichier" > fichier.txt

# Ayant un ajouté un fichier, nous l'avons en unstaged
git status

# Permet d'ajouter le fichier dans le prochain commit (staged)
git add fichier.txt

# Le fichier est prêt à être commit (en vert)
git status

# Commit du fichier, il est "sauvegardé"
git commit -m "ajout de fichier.txt"

# Le fichier est commit, plus aucun fichier visible (tous est unstaged)
git status 

git "modification du fichier" >> fichier.txt

# Le fichier est en modified et nécessite d'être ajouté au commit. 
git status

# Permet d'ajouter tout les fichiers présent dans le prochain commit
git add . 
git add -A
git add --all

# Dans le cas ou aucun nouveau fichier n'a été créé, on peut juste créer un nouveau commit 
# avec le parametre -a pour -all qui commit toutes les modifications de fichiers.
git commit -am "modification du fichier" 

# Permet de connaitre les différences entres l'état actuelle du projet et le commit précisé.
git diff <commit_id>
git diff <commit_id> <commit_id2>


# Editer le contenue du dernier commit
git commit --amend

# Editer le contenue du dernier commit
git commit --amend -m "edition du commit"

# Dans le cas ou l'on a oublié d'indexer un fichier on peut également 
# L'ajouter puis ré-éditer le dernier commit
git add mon_fichier_oublie.txt
git commit --amend --no-edit

# Pour ce placer à l'état du commit précisé 
git checkout <commit_id> 

