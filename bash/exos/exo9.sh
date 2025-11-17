# Question 1
echo "Bonjour tout le monde" > test
# Question 2
echo "Au revoir" >> test
# Question 3
#La commande find /etc -name hosts affiche des messages d'erreurs
find /etc -name hosts 2> err.txt
# Question 4
find /etc -name hosts > output.txt 2> err.txt