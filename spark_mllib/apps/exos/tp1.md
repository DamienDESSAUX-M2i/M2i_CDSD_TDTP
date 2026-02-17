# TP Plateforme de Streaming Musical

**Thème :** Vous êtes Data Engineer chez **SoundStream**, une plateforme de streaming musical. Votre mission est de préparer un pipeline MLlib de bout en bout pour recommander des titres aux utilisateurs, à partir d'un historique d'écoutes.

## Contexte métier

SoundStream collecte des données d'écoute pour chaque utilisateur : genre musical, durée d'écoute, heure de la journée, type d'abonnement, etc. Vous devez construire un pipeline MLlib qui transforme ces données brutes en vecteurs de features normalisés, prêts pour un futur modèle de recommandation.

## Description du dataset `streams.csv`

| Colonne             | Type   | Description                                                                |
| ------------------- | ------ | -------------------------------------------------------------------------- |
| `user_id`           | string | Identifiant utilisateur                                                    |
| `genre`             | string | Genre musical : `pop`, `rock`, `jazz`, `hiphop`, `classical`, `electronic` |
| `sub_type`          | string | Abonnement : `free`, `premium`, `family`                                   |
| `hour_of_day`       | int    | Heure d'écoute (0-23)                                                      |
| `listen_duration_s` | float  | Durée d'écoute en secondes (peut être null)                                |
| `nb_skips`          | int    | Nombre de skips de la session                                              |
| `nb_likes`          | int    | Nombre de likes (peut être null)                                           |
| `device_type`       | string | `mobile`, `desktop`, `smart_speaker`                                       |
| `explicit_content`  | int    | 1 = contenu explicite, 0 = non                                             |
| `engagement_score`  | float  | Score d'engagement 0-100 (**variable cible**)                              |

## SparkSession & Exploration

**1.1** Créer une `SparkSession` connectée au cluster Docker.

- `appName` : `"TP_SoundStream_J1"`
- `spark.executor.memory` : `1g`
- `spark.sql.shuffle.partitions` : `"8"`

**1.2** Charger `/data/streams.csv` avec inférence de schéma. Afficher :

- Le schéma complet
- Les 10 premières lignes
- Le nombre total d'écoutes et de colonnes

**1.3** Analyser la qualité des données :

- Calculer le **nombre et le pourcentage de nulls** pour chaque colonne
- Afficher les statistiques descriptives (`describe`) pour les colonnes numériques

**1.4** Analyser la distribution des variables catégorielles :

- Répartition des écoutes par `genre` (tri décroissant)
- Répartition des écoutes par `sub_type`
- Répartition des écoutes par `device_type`

**1.5** Analyser la variable cible `engagement_score` :

- Min, max, moyenne, médiane, Q1, Q3
- Distribution par tranche : `[0-25[`, `[25-50[`, `[50-75[`, `[75-100]`

## Partie 2 — Transformers MLlib

Appliquer **chaque transformer séparément** (fit + transform + show), puis les chaîner dans le Pipeline en Partie 3.

**2.1 — Imputer**
Remplacer les valeurs nulles de `listen_duration_s` et `nb_likes` par leur **médiane**.
Nommer les sorties `listen_duration_imp` et `nb_likes_imp`.

**2.2 — SQLTransformer**
Créer les features suivantes dans une seule requête SQL :

- `listen_minutes` : `listen_duration_imp / 60.0`
- `engagement_per_like` : `engagement_score / (nb_likes_imp + 1)`
- `peak_hour` : 1 si `hour_of_day` BETWEEN 18 AND 22, sinon 0

**2.3 — StringIndexer**
Encoder les colonnes `genre`, `sub_type` et `device_type` avec un `StringIndexer` **multi-colonnes** (un seul objet `StringIndexer`).

- `handleInvalid='keep'`

**2.4 — OneHotEncoder**
Appliquer un `OneHotEncoder` sur les colonnes `genre_idx` et `device_type_idx` (pas `sub_type_idx` — il restera en index ordinal).

- `dropLast=True`

**2.5 — VectorAssembler**
Assembler les features suivantes dans `features` :

- `listen_minutes`, `nb_skips`, `nb_likes_imp`, `explicit_content`, `peak_hour`, `hour_of_day`
- `engagement_per_like`
- `sub_type_idx` (ordinal)
- `genre_ohe`, `device_type_ohe`

Utiliser `handleInvalid='skip'`.

**2.6 — StandardScaler**
Appliquer un `StandardScaler` avec `withMean=True` et `withStd=True`.

**2.7 — Bucketizer**
Discrétiser `hour_of_day` en 4 tranches horaires :

- `[0, 6[`
- `[6, 12[`
- `[12, 18[`
- `[18, 24]`

Nommer la sortie `time_slot`.

## Partie 3 — Pipeline complet

**3.1** Diviser le dataset en **80% train / 20% test** (`seed=42`) **avant** de construire le Pipeline.

**3.2** Construire un `Pipeline` MLlib avec les stages suivants dans l'ordre :

1. `Imputer` (2.1)
2. `SQLTransformer` (2.2)
3. `Bucketizer` sur `hour_of_day` (2.7)
4. `StringIndexer` multi-colonnes (2.3)
5. `OneHotEncoder` (2.4)
6. `VectorAssembler` (2.5)
7. `StandardScaler` (2.6)

**3.3** Entraîner le Pipeline sur `train_df`

**3.4** Transformer `train_df` et `test_df` avec le `PipelineModel`.

**3.5** Sauvegarder le `PipelineModel` dans `/models/soundstream_pipeline`.
