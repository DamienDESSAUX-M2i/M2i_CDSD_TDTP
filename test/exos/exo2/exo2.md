# Exercice 03

- Créer une fonction `convertir_temperature(valeur, unite_source, unite_cible)` qui convertit une température entre Celsius, Fahrenheit et Kelvin.
- Unités acceptées : `"C"`, `"F"`, `"K"`
- Arrondir le résultat à 2 décimales
- Si l'unité source ou cible est invalide, lever une `ValueError`
- Si l'unité source = unité cible, retourner la valeur arrondie

## Formules de conversion

**De Celsius (C) vers :**

- Fahrenheit : `F = (C × 9/5) + 32`
- Kelvin : `K = C + 273.15`

**De Fahrenheit (F) vers :**

- Celsius : `C = (F - 32) × 5/9`
- Kelvin : `K = (F - 32) × 5/9 + 273.15`

**De Kelvin (K) vers :**

- Celsius : `C = K - 273.15`
- Fahrenheit : `F = (K - 273.15) × 9/5 + 32`

1. Tester au minimum 10 cas différents avec `@pytest.mark.parametrize`
2. Tester les cas d'erreur (unités invalides)
