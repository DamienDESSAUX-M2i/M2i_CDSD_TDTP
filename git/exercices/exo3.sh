# Question 1
git init
# Question 2
vim file1
git add file1
git commit -m "C1"
# Question 3
vim file1
git commit -am "C2"
# Question 4
git checkout -b feature C1_id
# Question 5
vim file1
git commit -am "C3"
# Question 6
git switch main
git merge feature
vim file1 # Gestion du conflit
git commit -am "Merge"