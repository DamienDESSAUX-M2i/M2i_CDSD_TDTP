# Exercice : Intervalles de Confiance — PizzaRapide

## Contexte

Tu travailles chez **PizzaRapide**, une chaîne de livraison de pizzas. Le directeur veut savoir combien de temps prennent les livraisons en moyenne pour décider s'il faut embaucher plus de livreurs.

Tu as relevé le temps de livraison (en minutes) de **30 commandes** sur une semaine :

```
32, 28, 35, 41, 29, 33, 37, 30, 26, 38,
34, 31, 27, 36, 33, 29, 42, 31, 35, 28,
30, 37, 33, 29, 34, 31, 36, 28, 32, 35
```

---

## Questions

### Question 1
Calcule la **moyenne** et l'**écart-type** des temps de livraison.

### Question 2
Calcule l'**erreur standard**.

### Question 3
Construis l'**intervalle de confiance à 95%** pour le temps moyen de livraison.

### Question 4
PizzaRapide promet sur son site : **"Livré en moins de 35 minutes en moyenne"**.
D'après ton intervalle de confiance, cette promesse est-elle réaliste ?

### Question 5
Le directeur veut un intervalle plus précis (plus étroit). Que doit-il faire ?

### Question 6
Construis maintenant les IC à **90%** et **99%**. Compare les 3 intervalles (90%, 95%, 99%). Que constates-tu ?

---

## Consignes

- Tous les calculs doivent être faits en Python.
- Formule à utiliser : **IC = moyenne ± z × erreur standard**
  - z = 1.645 pour 90%
  - z = 1.96 pour 95%
  - z = 2.576 pour 99%
- Justifie chaque réponse avec une phrase d'interprétation.
- Durée estimée : 30 minutes.
