# Question 1
git init
# Question 2
vim file1
git add file1
git commit -m "C1"
vim file1 # Modification
git commit -am "C2"
# Question 3
git switch -c B1 C1_id
# Question 4
vim file1
git commit -am "C3"
# Queston 5
git rebase main
vim file1 # Gestion des conflits
git commit -am "Rebase"