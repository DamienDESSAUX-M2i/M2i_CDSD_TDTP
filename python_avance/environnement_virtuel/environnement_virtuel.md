# Environnement virtuel Python

## Création environnement virtuel

```bash
python -m venv.venv
```
## Activation environnement virtuel

**Linux / Mac**

```bash
source ./.venv/Sripts/activate
```

**Windows**

```bash
./.venv/Sripts/activate
```

## Installation package

**Packages ETL**

```bash
pip install pandas openpyxl requests python-dotenv
pip install jupyter
```

## Enregistrement des dépendances

```bash
pip freeze > requirements.txt
```

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## .gitignore

```
.venv
```

## Config VSCode activation automatique de l'environnement virtuel

**Linux / Mac**

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

**Windows**

```json
{
    "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",
    "python.terminal.activateEnvironment": true
}
```
