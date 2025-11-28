# SQL Fondamental - Exercice 12

Exercice du module SQL de la formation Concepteur Développeur en Science des Données de M2I.

## Récupération du projet

L'exercice est hébergé sur GitHub. Pour récupérer l'exercice, placez-vous dans le répertoire de votre choix puis éxécutez la commande :

```bash
git clone https://github.com/DamienDESSAUX-M2i/M2i_CDSD_TDTP.git
```

Le chemin de l'exercice est `M2i_CDSD_TDTP/sql_fondamental/exos/exo12_v1/`.

## Lancement du projet sous Docker

Pour lancer le projet sous docker, placez-vous dans le répertoire `M2i_CDSD_TDTP/sql_fondamental/exos/exo12_v1/` puis éxécutez la commande :

```bash
docker compose up -d
```

Trois conteneurs `sql_fondamental_exo12_pgdb`, `sql_fondamental_exo12_pgadmin` et `sql_fondamental_exo12_app`, deux networks `sql_fondamental_exo12_db_network` et `sql_fondamental_exo12_app_network` et deux volumes `sql_fondamental_exo12_v_pgdb` et `sql_fondamental_exo12_v_pgadmin` seront créées.

## Commande pour exécuter les conteneurs.

Une fois les conteneurs `sql_fondamental_exo12_pgdb`, `sql_fondamental_exo12_pgadmin` et `sql_fondamental_exo12_app` construits, vous pouvez éxécutez le conteneur `sql_fondamental_exo12_app` avec la commande :

```bash
docker exec -it app python app.py
```

## Utilisation de l'application

Pour toutes les tables, les ids sont des nombres entiers positifs.

### Menu principal

Fonctionnalités :
- Utilisateurs : Accès au menu utilisateurs.
- Chansons : Accès au menu chansons.
- Playlists : Accès au menu playlists.
- Quitter. Mettre fin à l'application.

### Menu utilisateurs

Fonctionnalités :
- Afficher : Affichage des informations d'un utilisateur en fonction de son id.
- Ajouter : Ajout d'un utilisateur.
- Modifier : Modification d'un utilisateur en fonction de son id.
- Supprimer : Suppression d'un utilisateur en fonction de son  id.
- Quitter. Retour au menu principal.

### Menu chansons

Fonctionnalités :
- Afficher : Affichage des informations d'une chanson en fonction de son id.
- Ajouter : Ajout d'une chanson.
- Modifier : Modification d'une chanson en fonction de son id.
- Supprimer : Suppression d'une chanson en fonction de son  id.
- Quitter. Retour au menu principal.

### Menu playlists

Fonctionnalités :
- Afficher : Affichage des informations d'une playlist en fonction de son id.
- Ajouter : Ajout d'une playlist.
- Modifier : Modification d'une playlist en fonction de son id.
- Supprimer : Suppression d'une playlist en fonction de son  id.
- Remplir : Ajout d'une chanson dans une playlist en fonction des ids.
- Vider : Suppression d'une chanson dans une playlist en fonction des ids.
- Quitter. Retour au menu principal.