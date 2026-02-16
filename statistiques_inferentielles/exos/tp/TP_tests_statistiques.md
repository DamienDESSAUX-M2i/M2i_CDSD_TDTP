# TP : Analyse A/B Testing et Tests Statistiques
## Optimisation d'une Plateforme E-commerce

**Durée estimée** : 3-4 heures
**Niveau** : Data Analyst / Data Scientist
**Outils** : Python, pandas, scipy, matplotlib, seaborn

---

## Contexte Business

Vous êtes data analyst chez **TechShop**, une plateforme e-commerce spécialisée dans les produits électroniques. L'équipe produit souhaite optimiser plusieurs aspects du site pour améliorer les conversions et l'expérience utilisateur.

Vous avez été chargé(e) d'analyser **trois expérimentations** différentes menées sur le site :

1. **Test A/B** : Deux versions d'une page produit
2. **Test multivarié** : Quatre stratégies de promotion
3. **Test d'amélioration UX** : Temps de chargement selon différents algorithmes de recommandation

---

## Objectifs du TP

À l'issue de ce TP, vous serez capable de :
- Choisir le test statistique approprié selon le contexte
- Vérifier les conditions d'application des tests
- Interpréter les résultats et formuler des recommandations business
- Calculer la taille d'effet et la puissance statistique
- Réaliser des visualisations pour communiquer les résultats

---

## Partie 1 : Test A/B - Optimisation de la Page Produit

### Contexte
L'équipe UX a créé une nouvelle version de la page produit avec des images plus grandes et un bouton "Acheter" plus visible. Vous devez déterminer si cette nouvelle version améliore le **taux de conversion**.

- **Version A (Contrôle)** : Page actuelle
- **Version B (Traitement)** : Nouvelle page
- **Métrique** : Taux de conversion (achat / visite)
- **Période** : 14 jours
- **Trafic** : 50/50 split aléatoire

### Données

Créez un fichier `ab_test_data.csv` avec les données suivantes :

```python
import pandas as pd
import numpy as np

np.random.seed(42)

# Génération des données
n_visitors_A = 2500
n_visitors_B = 2500

# Version A : taux de conversion de 12%
conversions_A = np.random.binomial(1, 0.12, n_visitors_A)

# Version B : taux de conversion de 14.5% (amélioration)
conversions_B = np.random.binomial(1, 0.145, n_visitors_B)

# Montant des achats (pour ceux qui ont converti)
amounts_A = np.random.gamma(shape=2, scale=50, size=conversions_A.sum())
amounts_B = np.random.gamma(shape=2, scale=52, size=conversions_B.sum())

# DataFrame
df_ab = pd.DataFrame({
    'user_id': range(n_visitors_A + n_visitors_B),
    'variant': ['A'] * n_visitors_A + ['B'] * n_visitors_B,
    'converted': np.concatenate([conversions_A, conversions_B])
})

# Ajouter les montants
df_ab['purchase_amount'] = 0.0
df_ab.loc[df_ab['converted'] == 1, 'purchase_amount'] = np.concatenate([amounts_A, amounts_B])

df_ab.to_csv('ab_test_data.csv', index=False)
print(df_ab.head(10))
```

### Questions - Partie 1

**Q1.1** : Calculez le taux de conversion pour chaque variante. Quelle est la différence absolue et relative ?

**Q1.2** : Visualisez les taux de conversion avec un graphique en barres avec intervalles de confiance.

**Q1.3** : Avant de réaliser le test statistique, vérifiez les conditions d'application :
- Les observations sont-elles indépendantes ?
- L'échantillon est-il suffisamment grand ?

**Q1.4** : Réalisez un test de proportion (test z) pour comparer les taux de conversion. Formulez les hypothèses H0 et H1.

**Q1.5** : Interprétez la p-value obtenue. La différence est-elle statistiquement significative au seuil α = 0.05 ?

**Q1.6** : Calculez la **lift** (amélioration relative) et l'**intervalle de confiance à 95%** de la différence.

**Q1.7** : **Analyse du montant moyen des achats** : Comparez le montant moyen dépensé par les utilisateurs qui ont converti entre les deux variantes. Utilisez un test t de Student.

**Q1.8** : **Calcul de la puissance** : Avec la taille d'échantillon actuelle, quelle est la puissance statistique de votre test ?

**Q1.9** : **Recommandation Business** : Que recommandez-vous à l'équipe produit ? Considérez à la fois la significativité statistique et la significativité pratique.

---

## Partie 2 : ANOVA - Test Multi-Promotions

### Contexte
Le département marketing a testé **quatre stratégies de promotion** différentes pour augmenter les ventes :

- **Groupe A (Contrôle)** : Pas de promotion
- **Groupe B** : Réduction de 10%
- **Groupe C** : Livraison gratuite
- **Groupe D** : Réduction de 15% + livraison gratuite

Chaque client a été assigné aléatoirement à l'un des groupes. Vous devez analyser l'impact sur le **montant moyen du panier**.

### Données

```python
np.random.seed(123)

n_per_group = 300

# Montants moyens par groupe (avec effet réel)
group_A = np.random.normal(loc=85, scale=25, size=n_per_group)  # Contrôle
group_B = np.random.normal(loc=92, scale=27, size=n_per_group)  # -10%
group_C = np.random.normal(loc=98, scale=26, size=n_per_group)  # Livraison gratuite
group_D = np.random.normal(loc=105, scale=30, size=n_per_group) # -15% + livraison

df_promo = pd.DataFrame({
    'user_id': range(n_per_group * 4),
    'promotion_type': ['Control'] * n_per_group + ['Discount_10'] * n_per_group +
                      ['Free_Shipping'] * n_per_group + ['Combo'] * n_per_group,
    'basket_amount': np.concatenate([group_A, group_B, group_C, group_D])
})

df_promo.to_csv('promotion_test_data.csv', index=False)
print(df_promo.groupby('promotion_type')['basket_amount'].describe())
```

### Questions - Partie 2

**Q2.1** : Calculez les statistiques descriptives pour chaque groupe (moyenne, médiane, écart-type, quartiles).

**Q2.2** : Créez une visualisation comparative (boxplot ou violin plot) des montants par groupe de promotion.

**Q2.3** : **Vérification des conditions de l'ANOVA** :
- Testez la normalité des résidus (Shapiro-Wilk ou Q-Q plot)
- Testez l'homogénéité des variances (test de Levene)
- Les conditions sont-elles respectées ?

**Q2.4** : Réalisez une **ANOVA à un facteur** pour tester s'il existe une différence significative entre les groupes.

**Q2.5** : Si l'ANOVA est significative, réalisez des **tests post-hoc de Tukey** pour identifier quels groupes diffèrent significativement.

**Q2.6** : Calculez l'**eta-squared (η²)** pour mesurer la taille d'effet. Comment interprétez-vous cette valeur ?

**Q2.7** : **Scénario alternatif** : Si les conditions de l'ANOVA n'étaient pas respectées, quel test auriez-vous utilisé ? Réalisez ce test pour comparer.

**Q2.8** : **Recommandation Business** :
- Quelle stratégie de promotion recommandez-vous ?
- Analysez le ROI potentiel de chaque promotion
- Y a-t-il des promotions à éviter ?

---

## Partie 3 : Kruskal-Wallis - Performance des Algorithmes

### Contexte
L'équipe technique a développé **trois algorithmes de recommandation** différents et souhaite comparer leur performance en termes de **temps de chargement de la page**.

- **Algo A** : Filtrage collaboratif classique
- **Algo B** : Filtrage basé sur le contenu
- **Algo C** : Deep Learning (nouveau)

Les temps de chargement sont **fortement asymétriques** avec des outliers (pics de latence).

### Données

```python
np.random.seed(456)

n_samples = 200

# Temps de chargement en millisecondes (distributions non normales)
algo_A = np.random.gamma(shape=2, scale=100, size=n_samples)
algo_B = np.random.gamma(shape=1.8, scale=95, size=n_samples)
algo_C = np.random.gamma(shape=2.2, scale=110, size=n_samples)

# Ajouter quelques outliers
algo_A = np.append(algo_A, np.random.uniform(800, 1200, 10))
algo_B = np.append(algo_B, np.random.uniform(750, 1100, 10))
algo_C = np.append(algo_C, np.random.uniform(900, 1400, 10))

df_algo = pd.DataFrame({
    'request_id': range(len(algo_A) + len(algo_B) + len(algo_C)),
    'algorithm': ['Collaborative'] * len(algo_A) + ['Content'] * len(algo_B) + ['DeepLearning'] * len(algo_C),
    'loading_time_ms': np.concatenate([algo_A, algo_B, algo_C])
})

df_algo.to_csv('algorithm_performance_data.csv', index=False)
print(df_algo.groupby('algorithm')['loading_time_ms'].describe())
```

### Questions - Partie 3

**Q3.1** : Visualisez la distribution des temps de chargement pour chaque algorithme (histogrammes + boxplots).

**Q3.2** : Testez la normalité des données pour chaque groupe. Sont-elles normalement distribuées ?

**Q3.3** : Compte tenu de la distribution des données, justifiez le choix entre ANOVA et Kruskal-Wallis.

**Q3.4** : Réalisez le **test de Kruskal-Wallis** pour comparer les trois algorithmes.

**Q3.5** : Si le test est significatif, réalisez un **test de Dunn** (comparaisons post-hoc) pour identifier les différences par paires.

**Q3.6** : Calculez les **médianes et intervalles interquartiles** pour chaque algorithme.

**Q3.7** : **Comparaison avec ANOVA** : Pour l'apprentissage, réalisez également une ANOVA et comparez les résultats. Les conclusions sont-elles différentes ?

**Q3.8** : **Analyse des percentiles** : Calculez le 95e percentile pour chaque algorithme (temps maximum acceptable pour 95% des requêtes).

**Q3.9** : **Recommandation Technique** : Quel algorithme recommandez-vous de déployer en production ? Justifiez en tenant compte de la performance médiane et de la stabilité.

---

## Partie 4 : Test de Wilcoxon - Amélioration du Score de Satisfaction

### Contexte
Suite à une mise à jour de l'interface, vous souhaitez mesurer l'impact sur la **satisfaction utilisateur**. Vous avez collecté les scores de satisfaction (échelle 1-10) de **100 utilisateurs avant et après** la mise à jour (mesures appariées).

### Données

```python
np.random.seed(789)

n_users = 100

# Scores avant (moyenne 6.5)
scores_before = np.random.choice(range(1, 11), size=n_users, p=[0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.22, 0.15, 0.08, 0.05])

# Scores après (légère amélioration)
improvement = np.random.choice([-1, 0, 1, 2], size=n_users, p=[0.10, 0.30, 0.40, 0.20])
scores_after = np.clip(scores_before + improvement, 1, 10)

df_satisfaction = pd.DataFrame({
    'user_id': range(n_users),
    'score_before': scores_before,
    'score_after': scores_after,
    'difference': scores_after - scores_before
})

df_satisfaction.to_csv('satisfaction_scores_data.csv', index=False)
print(df_satisfaction[['score_before', 'score_after', 'difference']].describe())
```

### Questions - Partie 4

**Q4.1** : Calculez les statistiques descriptives des scores avant/après et de la différence.

**Q4.2** : Visualisez l'évolution des scores (graphique avant/après, histogramme des différences).

**Q4.3** : Testez la normalité de la **distribution des différences**. Est-elle normale ?

**Q4.4** : Justifiez le choix entre un **test t apparié** et un **test de Wilcoxon signé**.

**Q4.5** : Réalisez le **test de Wilcoxon pour échantillons appariés** (signed-rank test).

**Q4.6** : Calculez le **pourcentage d'utilisateurs** dont le score a augmenté, diminué ou resté stable.

**Q4.7** : Calculez la **taille d'effet** (r = Z / √N pour Wilcoxon).

**Q4.8** : **Recommandation** : La mise à jour a-t-elle significativement amélioré la satisfaction ? Faut-il la déployer à tous les utilisateurs ?

---

## Partie 5 : Analyse Complète et Reporting

### Mission Finale

Vous devez présenter vos résultats au **comité de direction**. Préparez un rapport synthétique incluant :

**Q5.1** : **Dashboard récapitulatif** : Créez une visualisation unique (figure avec subplots) résumant les 4 analyses.

**Q5.2** : **Tableau de synthèse** :

| Expérimentation | Test utilisé | P-value | Significatif ? | Taille d'effet | Recommandation |
|----------------|--------------|---------|----------------|----------------|----------------|
| Page produit   | ... | ... | ... | ... | ... |
| Promotions     | ... | ... | ... | ... | ... |
| Algorithmes    | ... | ... | ... | ... | ... |
| Satisfaction   | ... | ... | ... | ... | ... |

**Q5.3** : **Calcul de l'impact business global** :
- Revenus supplémentaires estimés si toutes les recommandations sont appliquées
- Priorisation des actions (quick wins vs. long terme)

**Q5.4** : **Limites et biais potentiels** :
- Identifiez les limites de chaque expérimentation
- Quels biais auraient pu affecter les résultats ?
- Quelles analyses complémentaires recommanderiez-vous ?

---

## Livrables Attendus

1. **Script Python** commenté avec toutes les analyses
2. **Rapport PDF** avec :
   - Visualisations claires et professionnelles
   - Interprétation des résultats statistiques
   - Recommandations business argumentées
3. **Présentation** (10 slides max) pour le comité de direction


---

## Ressources et Aide

### Bibliothèques Python recommandées

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, levene, ttest_ind, f_oneway, kruskal, wilcoxon
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.power import zt_ind_solve_power
import scikit_posthocs as sp  # Pour le test de Dunn
```

### Snippets utiles

**Test de normalité** :
```python
stat, p = shapiro(data)
print(f"Shapiro-Wilk: p-value = {p:.4f}")
if p > 0.05:
    print("Les données semblent normales")
```

**Test de Levene** :
```python
stat, p = levene(group1, group2, group3)
print(f"Levene: p-value = {p:.4f}")
```

**ANOVA** :
```python
f_stat, p_value = f_oneway(group1, group2, group3)
```

**Kruskal-Wallis** :
```python
h_stat, p_value = kruskal(group1, group2, group3)
```

**Test de Wilcoxon** :
```python
stat, p_value = wilcoxon(before, after)
```

**Taille d'effet (Cohen's d)** :
```python
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std
```

---

## Bonus (Optionnel)

**B1** : Réalisez une **simulation Monte Carlo** pour estimer la puissance statistique de votre test A/B.

**B2** : Implémentez un **test séquentiel** (Sequential A/B Testing) pour déterminer quand arrêter l'expérimentation.

**B3** : Analysez l'impact des **segments utilisateurs** (nouveaux vs. récurrents) sur les résultats du test A/B.

**B4** : Créez un **calculateur de sample size** interactif pour les futures expérimentations.

---

## Pour aller plus loin

- **Correction de Bonferroni** pour comparaisons multiples
- **Bootstrapping** pour intervalles de confiance robustes
- **Tests bayésiens** comme alternative aux tests fréquentistes
- **ANOVA à deux facteurs** pour tester plusieurs variables simultanément
- **Régression logistique** pour analyser les tests A/B avec covariables

---

**Bon courage !**
