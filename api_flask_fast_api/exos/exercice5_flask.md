## Exercice 5: Calculatrice API

**Énoncé**:
Créez une route `/calculate` qui accepte:
- `operation`: "add", "subtract", "multiply", "divide"
- `a`: premier nombre
- `b`: deuxième nombre

Exemple:
```bash
curl "http://localhost:5000/calculate?operation=add&a=10&b=5"
# {"operation": "add", "a": 10, "b": 5, "result": 15}

curl "http://localhost:5000/calculate?operation=divide&a=10&b=0"
# {"error": "Cannot divide by zero"}
```

