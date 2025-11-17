# clean est utilisé pour supprimer les fichiers non-suivies
git clean -n

# Supprimer les fichier non-suivi
git clean -f

# Supprimer les fichiers et dossiers non-suivi
git clean -fd

# Supprimer les fichiers présents dans le .gitignore
git clean -fx


# Annule un commit en créant un nouveau commit qui annule les modifications du commit spécifié
# Pratique quand on veut revenir en arrière sans supprimer l'historique
git revert <commit_id>
git revert HEAD # annule les modifications du commit précédent 


# Permet de réinitialiser l'index (staging) et l'arbre de travail au commit spécifié
git reset <commit_id>
git reset HEAD

# Revenir au commit précédent sans perdre les modifications locales et prêt au commit
git reset --soft HEAD

# Revenir au commit précédent sans perte mais l'on doit staged toutes les modifications avant commit
git reset --mixed HEAD
git reset HEAD

# Revenir à un commit spécifique en supprimant toutes le modications locales
# !!!! Attention car l'historique sera également effacé, pas de retour possible !!!!
git reset --hard HEAD
git reset --hard <commit_id>

# Si l'on souhaite réinitialiser un fichier à l'état du commit précédent, il suffit d'utiliser :
# Attention, les fichiers à restorer doivent être désindexé.
git restore <fichier>

# Si l'on souhaite réinitialiser tout le projet à son état initial (sans les modifications locales)
git restore .

