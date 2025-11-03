# Question 1
docker search nginx # nginx -> Official build of Nginx
docker pull nginx # par défaut applique le tag :latest
# Question 2
docker images # 1 image : nginx
# Question 3
docker rmi nginx # par défaut applique le tag :latest
# Question 4
docker search mysql # mysql -> Official
docker pull mysql
docker search redis # redis -> Official
docker pull mysql
# Question 5
docker images # 2 images : mysql et redis
# Question 6
docker inspect mysql # Port 3306
# Question 7
docker history mysql
# Question 8
docker search python # python -> Official
docker pull python # par défaut applique le tag :latest
docker inspect python # python version 3.14.0
docker history python