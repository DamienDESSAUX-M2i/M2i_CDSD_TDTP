## Exercice 2: Convertisseur de Température

**Énoncé**:
Créez une route `/convert/temp` qui accepte deux paramètres query:
- `value`: la température (nombre)
- `unit`: "c2f" (Celsius to Fahrenheit) ou "f2c" (Fahrenheit to Celsius)

Exemple:
```bash
curl "http://localhost:5000/convert/temp?value=25&unit=c2f"
# {"celsius": 25, "fahrenheit": 77.0}

curl "http://localhost:5000/convert/temp?value=77&unit=f2c"
# {"fahrenheit": 77, "celsius": 25.0}
```
