"""
Génération des données pour le TP Tests Statistiques
Module de Statistiques Inférentielles
"""

import pandas as pd
import numpy as np

print("=" * 80)
print(" GÉNÉRATION DES DONNÉES POUR LE TP")
print("=" * 80)

# ============================================================================
# PARTIE 1 : TEST A/B - PAGE PRODUIT
# ============================================================================
print("\nPartie 1 : Génération des données A/B Test")

np.random.seed(42)

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
print(f"  Fichier 'ab_test_data.csv' créé ({len(df_ab)} lignes)")
print(f"  Variante A: {n_visitors_A} visiteurs")
print(f"  Variante B: {n_visitors_B} visiteurs")

# ============================================================================
# PARTIE 2 : ANOVA - PROMOTIONS
# ============================================================================
print("\nPartie 2 : Génération des données Promotions")

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
print(f"  Fichier 'promotion_test_data.csv' créé ({len(df_promo)} lignes)")
print(f"  4 types de promotions, {n_per_group} observations par groupe")

# ============================================================================
# PARTIE 3 : KRUSKAL-WALLIS - ALGORITHMES
# ============================================================================
print("\nPartie 3 : Génération des données Algorithmes")

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
print(f"  Fichier 'algorithm_performance_data.csv' créé ({len(df_algo)} lignes)")
print(f"  3 algorithmes, {len(algo_A)} requêtes par algorithme")

# ============================================================================
# PARTIE 4 : WILCOXON - SATISFACTION
# ============================================================================
print("\nPartie 4 : Génération des données Satisfaction")

np.random.seed(789)

n_users = 100

# Scores avant (moyenne 6.5)
scores_before = np.random.choice(range(1, 11), size=n_users,
                                 p=[0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.22, 0.15, 0.08, 0.05])

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
print(f"  Fichier 'satisfaction_scores_data.csv' créé ({len(df_satisfaction)} lignes)")
print(f"  {n_users} utilisateurs avec scores avant/après")

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "=" * 80)
print(" RÉSUMÉ DES FICHIERS GÉNÉRÉS")
print("=" * 80)

files_info = [
    ("ab_test_data.csv", "Test A/B - Page produit", "5000 visiteurs (2 variantes)"),
    ("promotion_test_data.csv", "ANOVA - Promotions", "1200 clients (4 promotions)"),
    ("algorithm_performance_data.csv", "Kruskal-Wallis - Algorithmes", "630 requêtes (3 algos)"),
    ("satisfaction_scores_data.csv", "Wilcoxon - Satisfaction", "100 utilisateurs (avant/après)")
]

for filename, test, description in files_info:
    print(f"  {filename:40} | {test:25} | {description}")

print("\n" + "=" * 80)
print(" TOUS LES FICHIERS ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS !")
print(" Vous pouvez maintenant commencer le TP.")
print("=" * 80)
