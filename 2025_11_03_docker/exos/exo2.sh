# Question 2
docker search alpine # alpine -> Oficial
docker pull alpine
docker run -it --name my_alpine alpine
# Question 3
apk add git # installation git
cd home/
git clone https://github.com/DamienDESSAUX-M2i/M2i_CDSD_TDTP.git
cd M2i_CDSD_TDTP/
# Question 4
apk add vim
vim README.rm

## Pour pouvoir push, je dois créer un token sur GitHub puis exécuter les commandes suivantes :
# git remote set-url https://DamienDESSAUX-M2i:<token>@https://github.com/DamienDESSAUX-M2i/M2i_CDSD_TDTP.git
# git push