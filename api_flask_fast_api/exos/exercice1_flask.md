## Exercice 1: Hello World Multilingue

**Énoncé**:
Créez une application Flask avec une route `/hello/<language>` qui retourne un message "Hello" dans la langue spécifiée.

Exemple d'usage:
```bash
curl http://localhost:5000/hello/english
# {"message": "Hello!", "language": "english"}

curl http://localhost:5000/hello/french
# {"message": "Bonjour!", "language": "french"}
```

