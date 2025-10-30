# Question 1
git init
# Question 2
vim file1
git add file1
git commit -m "C1"
# Question 3
vim file2
git add file2
git commit -m "C2"
# Question 4
git log --oneline # 2 commits
# Question 5
vim file2
git commit -am "C3"
# Question 6
git reset C2_id
git restore file2
# Question 7
git log --oneline # 2 commits
# Question 8
git checkout C1_id
git branch feature # On peut aussi utiliser git branch feature C1_id
# Question 9
git commit -m "F1"
# Question 10
git log --oneline # 2 commits
# Question 11
git branch # 2 branches
# Question 12
git tag f1.0
# Question 13
git switch main
# Question 14
git tag # 1 tag
# Question 15
git branch -d feature
# Question 16
git branch # 1 branch