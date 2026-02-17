# Pipeline MLlib : Fitness Tracker

**Dataset** : `fitness_sessions.csv`
**Objectif** : Construire un pipeline MLlib complet pour preparer des donnees de seances de sport en vue de predire les calories brulees.

## Presentation du dataset

Le fichier `fitness_sessions.csv` contient des enregistrements de seances d'entrainement issues de trackers fitness. Chaque ligne represente une seance effectuee par un utilisateur.

| Colonne            | Type   | Description                                                                 |
| ------------------ | ------ | --------------------------------------------------------------------------- |
| `activity_type`    | string | Type d'activite : `running`, `cycling`, `swimming`, `yoga`, `weightlifting` |
| `intensity_level`  | string | Niveau d'intensite : `low`, `medium`, `high`                                |
| `duration_minutes` | float  | Duree de la seance en minutes (peut contenir des valeurs nulles)            |
| `heart_rate_avg`   | float  | Frequence cardiaque moyenne en bpm (peut contenir des valeurs nulles)       |
| `calories_burned`  | float  | Calories brulees — **variable cible**                                       |
| `distance_km`      | float  | Distance parcourue en km (0 pour yoga et weightlifting)                     |
| `steps_count`      | int    | Nombre de pas enregistres (peut contenir des valeurs nulles)                |
| `sleep_hours_prev` | float  | Heures de sommeil la nuit precedant la seance                               |
| `user_age`         | int    | Age de l'utilisateur                                                        |
| `is_morning`       | int    | 1 si la seance a eu lieu le matin (avant 12h), 0 sinon                      |

## Chargement et exploration

**1.** Creer une `SparkSession` connectee au cluster Docker avec les parametres suivants :

- `appName` : `"Exercice_Jour1_Fitness"`
- `master` : `spark://spark-master:7077`
- `spark.executor.memory` : `1g`

**2.** Lire le fichier `/data/fitness_sessions.csv` dans un DataFrame Spark avec inference automatique du schema et premiere ligne comme en-tete.

**3.** Afficher :

- Le schema complet du DataFrame
- Les 5 premieres lignes
- Le nombre total de lignes et de colonnes
- Les statistiques descriptives des colonnes numeriques

**4.** Calculer le nombre de valeurs nulles **par colonne** et afficher le resultat sous forme de tableau.

**5.** Analyser la variable cible `calories_burned` :

- Minimum, maximum, moyenne et mediane
- Calories moyennes brulees par `activity_type`

## Preparation des donnees

**6.** Utiliser un `Imputer` pour remplacer les valeurs nulles par leur **mediane** :

- Colonnes d'entree : `duration_minutes`, `heart_rate_avg`, `steps_count`
- Colonnes de sortie : `duration_imp`, `heart_rate_imp`, `steps_imp`
- Strategie : `median`

**7.** Creer deux nouvelles features via un `SQLTransformer` (en une seule requete SQL) :

- `effort_score` : `heart_rate_imp * duration_imp / 60.0`
- `is_active_sport` : 1 si `activity_type` est `running`, `cycling` ou `swimming`, 0 sinon

**8.** Encoder `activity_type` avec un `StringIndexer` (parametre `handleInvalid='keep'`), sortie `activity_idx`.

**9.** Encoder `intensity_level` avec un `StringIndexer` (sortie `intensity_idx`), puis appliquer un `OneHotEncoder` (`dropLast=True`), sortie `intensity_ohe`.

**10.** Assembler toutes les features dans une colonne `features` avec `VectorAssembler` :


**11.** Appliquer un `StandardScaler` sur la colonne `features` pour produire `features_scaled` (`withMean=True`, `withStd=True`).