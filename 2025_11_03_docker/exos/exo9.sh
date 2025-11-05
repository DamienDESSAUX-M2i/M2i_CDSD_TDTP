# Créer un volume Docker nommé data.
docker volume create data
docker volume ls # local data

# Lancer un premier conteneur basé sur alpine, en montant le volume.
docker run -it --name alpine1 -v data:/home alpine
docker ps # alpine1

# Ouvrir un terminal dans le premier conteneur et créer un fichier dans le volume partagé.
cd /home
echo "Text" > file1.txt
exit # quitter terminal
# CTRL+C quitter le conteneur

# Lancer un second conteneur utilisant le même volume.
docker run -it --name alpine2 -v data:/home alpine
docker ps # alpine1 alpine2

# Vérifier que le fichier créé par le premier conteneur est visible dans le second.
cd /home
cat file2.txt # Text

# Modifier le fichier depuis le second conteneur.
echo "Text supplémentaire" >> file1.txt
exit # quitter terminal
# CTRL+C quitter le conteneur

# Vérifier dans le premier conteneur que la modification est bien visible.
docker exec -it alpine1 sh
    cd /home
    cat file1.txt # Text\nText supplémentaire
    # CTRL+C quitter le conteneur

# Supprimer les conteneurs et le volume après le test.
docker stop alpine1 alpine2
docker rm alpine1 alpine2
docker ps # RAS
docker volume ls # local volume1
docker volume rm volume1
docker volume ls # RAS