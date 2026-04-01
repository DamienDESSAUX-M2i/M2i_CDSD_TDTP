# Babyfoot API 


## Technologies utilisées

- Python
- FastAPI
- Pydantic
- SQLite
- SQLAlchemy
- PyJWT

## Installation

Créer un environnement virtuel puis installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python run.py
```

L'application démarre sur :

- http://127.0.0.1:8000
- documentation Swagger : http://127.0.0.1:8000/docs

## Compte de démonstration déjà créé

- username : `admin`
- password : `admin123`

## Ordre conseillé pour tester

1. `POST /auth/register`
2. `POST /auth/login`
3. Copier le token JWT
4. Utiliser le bouton **Authorize** dans Swagger ou Bearer Token dans Postman
5. Tester les endpoints protégés

## Endpoints principaux

### Publics

- `GET /public/ping`
- `GET /public/info`

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Joueurs

- `POST /players`
- `GET /players`
- `GET /players/{player_id}`

### Équipes

- `POST /teams`
- `GET /teams`
- `GET /teams/{team_id}`

### Matchs

- `POST /matches`
- `GET /matches`
- `GET /matches/{match_id}`

### Classements

- `GET /rankings/players`
- `GET /rankings/teams`

## Exemples de requêtes

### Inscription

```json
{
  "username": "alice",
  "full_name": "Alice Martin",
  "password": "motdepasse123"
}
```

### Connexion

```json
{
  "username": "alice",
  "password": "motdepasse123"
}
```

### Création d'un joueur

```json
{
  "nickname": "Zizou"
}
```

### Création d'une équipe

```json
{
  "name": "Les Bleus",
  "player_1_id": 1,
  "player_2_id": 2
}
```

### Création d'un match joueur contre joueur

```json
{
  "match_type": "single",
  "participant_1_id": 1,
  "participant_2_id": 2,
  "score_1": 10,
  "score_2": 8
}
```

### Création d'un match équipe contre équipe

```json
{
  "match_type": "team",
  "participant_1_id": 1,
  "participant_2_id": 2,
  "score_1": 10,
  "score_2": 7
}
```


