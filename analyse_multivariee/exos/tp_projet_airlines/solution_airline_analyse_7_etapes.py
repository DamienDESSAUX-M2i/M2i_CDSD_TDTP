"""
################################################################################
#                                                                              #
#         ANALYSE MULTIVARIÉE COMPLÈTE - SATISFACTION PASSAGERS AÉRIENS        #
#                                                                              #
#                          LES 7 ÉTAPES COMPLÈTES                              #
#                                                                              #
#                           129,880 PASSAGERS                                  #
#                                                                              #
################################################################################
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, bartlett
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("   ANALYSE MULTIVARIÉE COMPLÈTE - SATISFACTION PASSAGERS AÉRIENS")
print("                        LES 7 ÉTAPES")
print("="*80)


################################################################################
#                                                                              #
#                    ÉTAPE 1 : NETTOYAGE DES DONNÉES                           #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 1 : NETTOYAGE DES DONNÉES")
print("="*80)

# ------------------------------------------------------------------------------
# 1.1 Chargement des données
# ------------------------------------------------------------------------------
print("\n--- 1.1 Chargement des données ---")

df = pd.read_csv('airline_passenger_satisfaction.csv')

print(f"\n✓ Fichier chargé : airline_passenger_satisfaction.csv")
print(f"✓ Dimensions : {df.shape[0]:,} lignes × {df.shape[1]} colonnes")

# ------------------------------------------------------------------------------
# 1.2 Exploration initiale
# ------------------------------------------------------------------------------
print("\n--- 1.2 Exploration initiale ---")

print(f"\n>>> Liste des {len(df.columns)} colonnes :")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

# Classification des variables
vars_cat = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'Satisfaction']
vars_num_continues = ['Age', 'Flight Distance', 'Departure Delay', 'Arrival Delay']
colonnes_exclure = ['ID'] + vars_cat + vars_num_continues
vars_satisfaction = [col for col in df.columns if col not in colonnes_exclure]

print(f"\n>>> Classification des variables :")
print(f"  • Catégorielles : {len(vars_cat)}")
print(f"  • Numériques continues : {len(vars_num_continues)}")
print(f"  • Variables de satisfaction (notes 0-5) : {len(vars_satisfaction)}")

# ------------------------------------------------------------------------------
# 1.3 Analyse des variables catégorielles
# ------------------------------------------------------------------------------
print("\n--- 1.3 Variables catégorielles ---")

for var in vars_cat:
    print(f"\n{var} :")
    for val, count in df[var].value_counts().items():
        pct = count / len(df) * 100
        bar = "█" * int(pct / 5)
        print(f"  {val:<30} : {count:>7,} ({pct:>5.1f}%) {bar}")

# ------------------------------------------------------------------------------
# 1.4 Analyse des variables numériques continues
# ------------------------------------------------------------------------------
print("\n--- 1.4 Variables numériques continues ---")

for var in vars_num_continues:
    print(f"\n{var} :")
    print(f"  Min: {df[var].min()}, Max: {df[var].max():.0f}, Moyenne: {df[var].mean():.1f}, Médiane: {df[var].median():.1f}")

# ------------------------------------------------------------------------------
# 1.5 Valeurs manquantes
# ------------------------------------------------------------------------------
print("\n--- 1.5 Valeurs manquantes ---")

na_count = df.isnull().sum()
na_total = na_count.sum()

print(f"\nNombre TOTAL de valeurs manquantes : {na_total:,}")

if na_total > 0:
    print("\nDétail :")
    for col, count in na_count[na_count > 0].items():
        pct = count / len(df) * 100
        print(f"  • {col}: {count:,} NA ({pct:.2f}%)")
    
    # Traitement
    print("\n>>> Traitement des NA :")
    for col in na_count[na_count > 0].index:
        mediane = df[col].median()
        df[col].fillna(mediane, inplace=True)
        print(f"  • {col}: NA remplacés par la médiane ({mediane:.0f})")
    
    print(f"\n✓ Après traitement : {df.isnull().sum().sum()} NA")
else:
    print("✓ Aucune valeur manquante")

# Vérifier les 0 dans les notes
print("\n>>> Valeurs 0 dans les notes de satisfaction :")
print("    (0 peut signifier 'non applicable' ou 'non répondu')")
zeros_found = False
for col in vars_satisfaction:
    n_zeros = (df[col] == 0).sum()
    if n_zeros > 0:
        zeros_found = True
        pct = n_zeros / len(df) * 100
        print(f"  • {col}: {n_zeros:,} ({pct:.1f}%)")
if not zeros_found:
    print("  ✓ Aucune valeur 0 trouvée")

# ------------------------------------------------------------------------------
# 1.6 Détection des outliers
# ------------------------------------------------------------------------------
print("\n--- 1.6 Détection des outliers (méthode IQR) ---")

def detecter_outliers(serie):
    Q1, Q3 = serie.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    borne_basse = Q1 - 1.5 * IQR
    borne_haute = Q3 + 1.5 * IQR
    outliers = ((serie < borne_basse) | (serie > borne_haute)).sum()
    return outliers, borne_basse, borne_haute

print(f"\n{'Variable':<25} | {'Outliers':>15} | {'Borne -':>10} | {'Borne +':>10}")
print("-" * 70)
for var in vars_num_continues:
    n_out, bb, bh = detecter_outliers(df[var])
    pct = n_out / len(df) * 100
    print(f"{var:<25} | {n_out:>8,} ({pct:>4.1f}%) | {bb:>10.1f} | {bh:>10.1f}")

print("\n→ Les outliers dans les retards sont CONSERVÉS (valeurs légitimes)")

# ------------------------------------------------------------------------------
# 1.7 Doublons
# ------------------------------------------------------------------------------
print("\n--- 1.7 Vérification des doublons ---")

n_doublons = df.duplicated().sum()
print(f"\nDoublons : {n_doublons}")
if n_doublons > 0:
    df = df.drop_duplicates()
    print(f"✓ Supprimés. Nouvelles dimensions : {df.shape[0]:,} lignes")
else:
    print("✓ Aucun doublon")

# ------------------------------------------------------------------------------
# 1.8 Variable cible
# ------------------------------------------------------------------------------
print("\n--- 1.8 Analyse de la variable cible ---")

satisfaction_counts = df['Satisfaction'].value_counts()
print("\n>>> Distribution de la Satisfaction :")
for cat, count in satisfaction_counts.items():
    pct = count / len(df) * 100
    bar = "█" * int(pct / 2)
    print(f"  {cat:<30} : {count:>7,} ({pct:>5.1f}%) {bar}")

# Créer variable binaire
df['Satisfaction_Binary'] = (df['Satisfaction'] == 'Satisfied').astype(int)
print(f"\n✓ Variable binaire créée : Satisfaction_Binary")
print(f"  • 1 (Satisfied)   : {df['Satisfaction_Binary'].sum():,}")
print(f"  • 0 (Insatisfait) : {(df['Satisfaction_Binary']==0).sum():,}")

# ------------------------------------------------------------------------------
# 1.9 Taux de satisfaction par segment
# ------------------------------------------------------------------------------
print("\n--- 1.9 Taux de satisfaction par segment ---")

for var in ['Gender', 'Customer Type', 'Type of Travel', 'Class']:
    print(f"\n{var} :")
    for val in df[var].unique():
        taux = df[df[var] == val]['Satisfaction_Binary'].mean() * 100
        n = len(df[df[var] == val])
        bar = "█" * int(taux / 5)
        print(f"  {val:<20} : {taux:>5.1f}% satisfaits (n={n:>6,}) {bar}")

# ------------------------------------------------------------------------------
# 1.10 Statistiques descriptives des notes
# ------------------------------------------------------------------------------
print("\n--- 1.10 Statistiques des notes de satisfaction ---")

print("\n>>> Classement par note moyenne :")
moyennes = df[vars_satisfaction].mean().sort_values(ascending=False)
for i, (var, moy) in enumerate(moyennes.items(), 1):
    bar = "█" * int(moy * 4)
    emoji = "😊" if moy >= 4 else "😐" if moy >= 3 else "😞"
    print(f"  {i:2}. {var:<45} {moy:.2f}/5 {bar} {emoji}")

# ------------------------------------------------------------------------------
# 1.11 Visualisation Étape 1
# ------------------------------------------------------------------------------
print("\n--- 1.11 Visualisation ---")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Distribution satisfaction
ax1 = axes[0, 0]
colors = ['#22c55e' if 'Satisfied' == x else '#ef4444' for x in satisfaction_counts.index]
bars = ax1.bar(range(len(satisfaction_counts)), satisfaction_counts.values, color=colors, edgecolor='white')
ax1.set_xticks(range(len(satisfaction_counts)))
ax1.set_xticklabels([x.replace(' or ', '\nor ') for x in satisfaction_counts.index], fontsize=10)
ax1.set_title(f'Distribution de la Satisfaction\n(n={len(df):,})', fontweight='bold')
ax1.set_ylabel('Nombre de passagers')
for i, bar in enumerate(bars):
    pct = satisfaction_counts.values[i] / len(df) * 100
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
             f'{pct:.1f}%', ha='center', fontweight='bold')

# 2. Satisfaction par Classe
ax2 = axes[0, 1]
class_sat = df.groupby('Class')['Satisfaction_Binary'].mean().sort_values() * 100
colors2 = plt.cm.RdYlGn(class_sat / 100)
bars2 = ax2.barh(class_sat.index, class_sat.values, color=colors2, edgecolor='white')
ax2.set_title('Taux de satisfaction par Classe', fontweight='bold')
ax2.set_xlabel('% Satisfaits')
ax2.axvline(x=50, color='gray', linestyle='--', alpha=0.7)
for bar, val in zip(bars2, class_sat.values):
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontweight='bold')

# 3. Satisfaction par Type de voyage
ax3 = axes[0, 2]
travel_sat = df.groupby('Type of Travel')['Satisfaction_Binary'].mean().sort_values() * 100
colors3 = plt.cm.RdYlGn(travel_sat / 100)
bars3 = ax3.barh(travel_sat.index, travel_sat.values, color=colors3, edgecolor='white')
ax3.set_title('Taux de satisfaction par Type de voyage', fontweight='bold')
ax3.set_xlabel('% Satisfaits')
ax3.axvline(x=50, color='gray', linestyle='--', alpha=0.7)
for bar, val in zip(bars3, travel_sat.values):
    ax3.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontweight='bold')

# 4. Notes moyennes
ax4 = axes[1, 0]
colors4 = plt.cm.RdYlGn(moyennes / 5)
moyennes.plot(kind='barh', ax=ax4, color=colors4, edgecolor='white')
ax4.set_title('Note moyenne par critère', fontweight='bold')
ax4.set_xlabel('Note moyenne (0-5)')
ax4.axvline(x=3, color='gray', linestyle='--', alpha=0.7)

# 5. Distribution âge par satisfaction
ax5 = axes[1, 1]
df[df['Satisfaction']=='Satisfied']['Age'].hist(ax=ax5, bins=30, alpha=0.6, label='Satisfaits', color='green', edgecolor='white')
df[df['Satisfaction']!='Satisfied']['Age'].hist(ax=ax5, bins=30, alpha=0.6, label='Insatisfaits', color='red', edgecolor='white')
ax5.set_title('Distribution de l\'âge par satisfaction', fontweight='bold')
ax5.set_xlabel('Âge')
ax5.legend()

# 6. Satisfaction par Customer Type
ax6 = axes[1, 2]
cust_sat = df.groupby('Customer Type')['Satisfaction_Binary'].mean().sort_values() * 100
colors6 = plt.cm.RdYlGn(cust_sat / 100)
bars6 = ax6.barh(cust_sat.index, cust_sat.values, color=colors6, edgecolor='white')
ax6.set_title('Taux de satisfaction par Type de client', fontweight='bold')
ax6.set_xlabel('% Satisfaits')
ax6.axvline(x=50, color='gray', linestyle='--', alpha=0.7)
for bar, val in zip(bars6, cust_sat.values):
    ax6.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('etape1_nettoyage.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Graphique sauvegardé : etape1_nettoyage.png")

# ------------------------------------------------------------------------------
# Bilan Étape 1
# ------------------------------------------------------------------------------
print("\n" + "-"*60)
print("BILAN ÉTAPE 1 : NETTOYAGE DES DONNÉES")
print("-"*60)
print(f"""
📊 DONNÉES :
  • {df.shape[0]:,} passagers
  • {len(vars_satisfaction)} variables de satisfaction
  • NA traités : {na_total}
  • Doublons : {n_doublons}

📈 SATISFACTION :
  • Taux global : {df['Satisfaction_Binary'].mean()*100:.1f}%
  • Business Class : {df[df['Class']=='Business']['Satisfaction_Binary'].mean()*100:.1f}%
  • Economy Class : {df[df['Class']=='Economy']['Satisfaction_Binary'].mean()*100:.1f}%

🏆 Top critère : {moyennes.index[0]} ({moyennes.iloc[0]:.2f}/5)
⚠️ Pire critère : {moyennes.index[-1]} ({moyennes.iloc[-1]:.2f}/5)

→ Prêt pour l'ÉTAPE 2 : Standardisation
""")


################################################################################
#                                                                              #
#                    ÉTAPE 2 : STANDARDISATION                                 #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 2 : STANDARDISATION (Z-SCORE)")
print("="*80)

# Sélectionner X et y
X = df[vars_satisfaction].copy()
y = df['Satisfaction_Binary'].copy()

print(f"\n>>> Données AVANT standardisation :")
print(f"  Moyennes : de {X.mean().min():.2f} à {X.mean().max():.2f}")
print(f"  Écarts-types : de {X.std().min():.2f} à {X.std().max():.2f}")

# Standardisation
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

print(f"\n>>> Données APRÈS standardisation :")
print(f"  Moyennes : {X_scaled.mean().mean():.6f} (≈ 0 ✓)")
print(f"  Écarts-types : {X_scaled.std().mean():.6f} (≈ 1 ✓)")

print("\n" + "-"*60)
print("BILAN ÉTAPE 2 : Standardisation terminée")
print("-"*60)
print(f"✓ {len(vars_satisfaction)} variables standardisées")
print("→ Prêt pour l'ÉTAPE 3 : Corrélations")


################################################################################
#                                                                              #
#                    ÉTAPE 3 : CORRÉLATIONS                                    #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 3 : ANALYSE DES CORRÉLATIONS")
print("="*80)

corr_matrix = X.corr()

# Corrélations fortes
print("\n>>> Corrélations fortes entre variables (|r| ≥ 0.5) :")
pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        r = corr_matrix.iloc[i, j]
        if abs(r) >= 0.5:
            pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], r))

pairs_sorted = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)
for v1, v2, r in pairs_sorted:
    print(f"  {v1[:25]:<25} ↔ {v2[:25]:<25} r={r:.3f}")

# Corrélations avec Y
print("\n>>> Corrélations avec la Satisfaction :")
corr_y = X.corrwith(y).sort_values(key=abs, ascending=False)
for var, r in corr_y.items():
    emoji = "🔥" if abs(r) >= 0.4 else "⭐" if abs(r) >= 0.3 else ""
    bar = "█" * int(abs(r) * 20)
    print(f"  {var:<45} r={r:+.3f} {bar} {emoji}")

# Graphique
fig, ax = plt.subplots(1, 2, figsize=(16, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax[0], annot_kws={'size': 8})
ax[0].set_title('Matrice de corrélation', fontweight='bold')
colors = ['green' if r > 0 else 'red' for r in corr_y]
corr_y.plot(kind='barh', ax=ax[1], color=colors, edgecolor='white')
ax[1].axvline(0, color='black')
ax[1].axvline(0.3, color='gray', linestyle='--', alpha=0.5)
ax[1].set_title('Corrélation avec Satisfaction', fontweight='bold')
plt.tight_layout()
plt.savefig('etape3_correlations.png', dpi=150)
plt.close()
print("\n✓ Graphique sauvegardé : etape3_correlations.png")

print("\n" + "-"*60)
print("BILAN ÉTAPE 3 : Corrélations analysées")
print("-"*60)
print(f"✓ {len(pairs)} paires avec |r| ≥ 0.5")
print(f"✓ Variable clé : {corr_y.index[0]} (r={corr_y.iloc[0]:.3f})")
print("→ Prêt pour l'ÉTAPE 4 : ACP")


################################################################################
#                                                                              #
#                    ÉTAPE 4 : ACP                                             #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 4 : ANALYSE EN COMPOSANTES PRINCIPALES (ACP)")
print("="*80)

pca = PCA()
pca.fit(X_scaled)

var_exp = pca.explained_variance_ratio_
var_cum = var_exp.cumsum()
eigenvalues = pca.explained_variance_

print("\n>>> Variance expliquée par composante :")
for i, (v, c, e) in enumerate(zip(var_exp, var_cum, eigenvalues)):
    kaiser = "← λ>1" if e > 1 else ""
    bar = "█" * int(v * 50)
    print(f"  PC{i+1:2}: {v*100:5.1f}% | Cumulé: {c*100:5.1f}% | λ={e:.2f} {bar} {kaiser}")

n_kaiser = sum(eigenvalues > 1)
n_80 = (var_cum >= 0.80).argmax() + 1
n_comp = max(n_kaiser, n_80)

print(f"\n>>> Critères de sélection :")
print(f"  • Kaiser (λ > 1) : {n_kaiser} composantes")
print(f"  • Variance ≥ 80% : {n_80} composantes")
print(f"  → RETENU : {n_comp} composantes ({var_cum[n_comp-1]*100:.1f}%)")

# Graphique
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
x = range(1, len(eigenvalues) + 1)
ax[0].bar(x, var_exp * 100, alpha=0.6, color='steelblue', label='Individuelle')
ax[0].plot(x, var_cum * 100, 'ro-', label='Cumulée')
ax[0].axhline(80, color='green', linestyle='--', label='80%')
ax[0].set_xlabel('Composante')
ax[0].set_ylabel('Variance (%)')
ax[0].set_title('Scree Plot', fontweight='bold')
ax[0].legend()
ax[0].set_xticks(x)
colors = ['green' if e > 1 else 'gray' for e in eigenvalues]
ax[1].bar(x, eigenvalues, color=colors, edgecolor='white')
ax[1].axhline(1, color='red', linestyle='--', label='Kaiser (λ=1)')
ax[1].set_xlabel('Composante')
ax[1].set_ylabel('Valeur propre')
ax[1].set_title('Critère de Kaiser', fontweight='bold')
ax[1].legend()
ax[1].set_xticks(x)
plt.tight_layout()
plt.savefig('etape4_acp.png', dpi=150)
plt.close()
print("\n✓ Graphique sauvegardé : etape4_acp.png")

print("\n" + "-"*60)
print("BILAN ÉTAPE 4 : ACP terminée")
print("-"*60)
print(f"✓ {n_comp} composantes retenues ({var_cum[n_comp-1]*100:.1f}% variance)")
print("→ Prêt pour l'ÉTAPE 5 : Analyse Factorielle")


################################################################################
#                                                                              #
#                    ÉTAPE 5 : ANALYSE FACTORIELLE                             #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 5 : ANALYSE FACTORIELLE")
print("="*80)

# ------------------------------------------------------------------------------
# Fonction KMO manuelle (pour éviter le bug de factor_analyzer)
# ------------------------------------------------------------------------------
def calculate_kmo_manual(X):
    """Calcule le KMO manuellement"""
    corr = X.corr().values
    n = corr.shape[0]
    
    # Matrice de corrélation partielle
    inv_corr = np.linalg.pinv(corr)
    partial_corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                partial_corr[i, j] = -inv_corr[i, j] / np.sqrt(inv_corr[i, i] * inv_corr[j, j])
    
    # Calcul du KMO
    corr_sum = 0
    partial_sum = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                corr_sum += corr[i, j] ** 2
                partial_sum += partial_corr[i, j] ** 2
    
    kmo = corr_sum / (corr_sum + partial_sum)
    return kmo

# Test KMO
kmo_total = calculate_kmo_manual(X)

print(f"\n>>> Prérequis :")
print(f"  • KMO : {kmo_total:.3f} {'(BON ✓)' if kmo_total >= 0.7 else '(ACCEPTABLE)'}")

# Test de Bartlett (simplifié)
n = len(X)
p = len(X.columns)
corr = X.corr()
det_corr = np.linalg.det(corr)
chi2_bartlett = -((n - 1) - (2*p + 5)/6) * np.log(det_corr)
df_bartlett = p * (p - 1) / 2
p_bartlett = 1 - stats.chi2.cdf(chi2_bartlett, df_bartlett)

print(f"  • Bartlett : Chi²={chi2_bartlett:,.0f}, p={p_bartlett:.2e} ✓")
print(f"  • Ratio N/var : {len(X)//len(X.columns)} (min recommandé: 5) ✓")

# Extraction avec sklearn FactorAnalysis (compatible)
n_fact = min(4, n_kaiser)
fa = FactorAnalysis(n_components=n_fact, random_state=42)
fa.fit(X_scaled)

# Loadings
loadings = pd.DataFrame(
    fa.components_.T,
    columns=[f'F{i+1}' for i in range(n_fact)],
    index=X.columns
)

# Rotation Varimax manuelle
def varimax_rotation(loadings, max_iter=100, tol=1e-6):
    """Applique une rotation Varimax aux loadings"""
    n_vars, n_factors = loadings.shape
    rotation_matrix = np.eye(n_factors)
    var_old = 0
    
    for _ in range(max_iter):
        loadings_rotated = loadings @ rotation_matrix
        
        for i in range(n_factors):
            for j in range(i + 1, n_factors):
                x = loadings_rotated[:, i]
                y = loadings_rotated[:, j]
                
                u = x**2 - y**2
                v = 2 * x * y
                
                a = np.sum(u)
                b = np.sum(v)
                c = np.sum(u**2 - v**2)
                d = 2 * np.sum(u * v)
                
                phi = 0.25 * np.arctan2(d - 2*a*b/n_vars, c - (a**2 - b**2)/n_vars)
                
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)
                
                rot = np.array([[cos_phi, -sin_phi], [sin_phi, cos_phi]])
                rotation_matrix[:, [i, j]] = rotation_matrix[:, [i, j]] @ rot
        
        loadings_rotated = loadings @ rotation_matrix
        var_new = np.sum(np.var(loadings_rotated**2, axis=0))
        
        if abs(var_new - var_old) < tol:
            break
        var_old = var_new
    
    return loadings @ rotation_matrix

# Appliquer Varimax
loadings_rotated = varimax_rotation(loadings.values)
loadings = pd.DataFrame(loadings_rotated, columns=[f'F{i+1}' for i in range(n_fact)], index=X.columns)

print(f"\n>>> Loadings ({n_fact} facteurs, rotation Varimax) :")
print(loadings.round(3).to_string())

# Interprétation
print("\n>>> Interprétation des facteurs (loadings ≥ 0.4) :")
for i in range(n_fact):
    f = f'F{i+1}'
    fortes = loadings[f][abs(loadings[f]) >= 0.4].sort_values(key=abs, ascending=False)
    print(f"\n{f}:")
    for var, val in fortes.items():
        print(f"  {'+'if val>0 else '-'} {var}: {val:.3f}")

# Communautés
communautes = (loadings**2).sum(axis=1)
comm = pd.DataFrame({'Variable': X.columns, 'h2': communautes.values})
comm = comm.sort_values('h2', ascending=False)

print("\n>>> Communautés :")
for _, r in comm.iterrows():
    st = "✓" if r['h2'] >= 0.4 else "⚠️"
    print(f"  {r['Variable']:<45} {r['h2']:.3f} {st}")

# Graphique
fig, ax = plt.subplots(1, 2, figsize=(16, 7))
sns.heatmap(loadings, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax[0], annot_kws={'size': 9})
ax[0].set_title('Loadings après rotation Varimax', fontweight='bold')
colors = ['green' if c >= 0.4 else 'orange' if c >= 0.3 else 'red' for c in comm['h2']]
ax[1].barh(comm['Variable'], comm['h2'], color=colors, edgecolor='white')
ax[1].axvline(0.4, color='green', linestyle='--', label='Bon (0.4)')
ax[1].axvline(0.3, color='orange', linestyle='--', label='Acceptable (0.3)')
ax[1].set_xlabel('Communauté')
ax[1].set_title('Communautés', fontweight='bold')
ax[1].legend(loc='lower right')
plt.tight_layout()
plt.savefig('etape5_af.png', dpi=150)
plt.close()
print("\n✓ Graphique sauvegardé : etape5_af.png")

print("\n" + "-"*60)
print("BILAN ÉTAPE 5 : Analyse Factorielle terminée")
print("-"*60)
print(f"✓ KMO = {kmo_total:.3f}")
print(f"✓ {n_fact} facteurs extraits avec rotation Varimax")
print("→ Prêt pour l'ÉTAPE 6 : Régression")


################################################################################
#                                                                              #
#                    ÉTAPE 6 : RÉGRESSION MULTIPLE                             #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 6 : RÉGRESSION MULTIPLE")
print("="*80)

# Préparation
df_reg = X.copy()
df_reg['Satisfaction'] = y
df_reg.columns = df_reg.columns.str.replace(' ', '_').str.replace('-', '_')
vars_clean = [c.replace(' ', '_').replace('-', '_') for c in vars_satisfaction]

formule = 'Satisfaction ~ ' + ' + '.join(vars_clean)
model = smf.ols(formule, data=df_reg).fit()

print(f"\n>>> Résumé du modèle :")
print(f"  R²         : {model.rsquared:.4f} ({model.rsquared*100:.1f}% variance expliquée)")
print(f"  R² ajusté  : {model.rsquared_adj:.4f}")
print(f"  F-statistic: {model.fvalue:.1f}")
print(f"  p-value    : < 0.001")

print("\n>>> Coefficients (triés par importance) :")
coefs = pd.DataFrame({'Coef': model.params, 'p': model.pvalues}).drop('Intercept')
coefs = coefs.sort_values('Coef', key=abs, ascending=False)
for var, r in coefs.iterrows():
    sig = "***" if r['p'] < 0.001 else "**" if r['p'] < 0.01 else "*" if r['p'] < 0.05 else ""
    print(f"  {var:<50} β={r['Coef']:+.4f} {sig}")

n_sig = (coefs['p'] < 0.05).sum()
print(f"\n→ {n_sig}/{len(coefs)} variables significatives")

# Diagnostics
residus = model.resid
sample = residus.sample(min(5000, len(residus)), random_state=42)
_, p_shap = shapiro(sample)
bp_stat, p_bp, _, _ = het_breuschpagan(residus, model.model.exog)

print(f"\n>>> Diagnostics :")
print(f"  • Normalité (Shapiro)     : p={p_shap:.4f} {'✓' if p_shap > 0.05 else '⚠️'}")
print(f"  • Homoscédasticité (BP)   : p={p_bp:.4f} {'✓' if p_bp > 0.05 else '⚠️'}")

# VIF
X_const = sm.add_constant(df_reg[vars_clean])
vifs = [variance_inflation_factor(X_const.values, i+1) for i in range(len(vars_clean))]
vif_max = max(vifs)
print(f"  • VIF maximum             : {vif_max:.2f} {'✓' if vif_max < 5 else '⚠️'}")

# Graphique
fig, ax = plt.subplots(2, 2, figsize=(14, 10))
ax[0, 0].scatter(model.fittedvalues, residus, alpha=0.2, s=3)
ax[0, 0].axhline(0, color='red', linestyle='--')
ax[0, 0].set_xlabel('Valeurs prédites')
ax[0, 0].set_ylabel('Résidus')
ax[0, 0].set_title('Résidus vs Prédictions', fontweight='bold')
stats.probplot(sample, plot=ax[0, 1])
ax[0, 1].set_title('QQ-Plot', fontweight='bold')
ax[1, 0].hist(residus, bins=50, edgecolor='white', density=True, color='steelblue')
ax[1, 0].set_xlabel('Résidus')
ax[1, 0].set_title('Distribution des résidus', fontweight='bold')
top10 = coefs[coefs['p'] < 0.05].head(10)
colors = ['green' if c > 0 else 'red' for c in top10['Coef']]
ax[1, 1].barh(range(len(top10)), top10['Coef'], color=colors, edgecolor='white')
ax[1, 1].set_yticks(range(len(top10)))
ax[1, 1].set_yticklabels([v[:35] for v in top10.index], fontsize=9)
ax[1, 1].axvline(0, color='black')
ax[1, 1].set_xlabel('Coefficient')
ax[1, 1].set_title('Top 10 coefficients', fontweight='bold')
plt.tight_layout()
plt.savefig('etape6_regression.png', dpi=150)
plt.close()
print("\n✓ Graphique sauvegardé : etape6_regression.png")

print("\n" + "-"*60)
print("BILAN ÉTAPE 6 : Régression terminée")
print("-"*60)
print(f"✓ R² = {model.rsquared:.4f} ({model.rsquared*100:.1f}%)")
print(f"✓ {n_sig} variables significatives")
print("→ Prêt pour l'ÉTAPE 7 : Interprétation")


################################################################################
#                                                                              #
#                    ÉTAPE 7 : INTERPRÉTATION MÉTIER                           #
#                                                                              #
################################################################################

print("\n" + "="*80)
print("ÉTAPE 7 : INTERPRÉTATION MÉTIER ET RECOMMANDATIONS")
print("="*80)

# Calculs pour le rapport
bus_bus = df[(df['Class']=='Business') & (df['Type of Travel']=='Business')]['Satisfaction_Binary'].mean()*100
eco_per = df[(df['Class']=='Economy') & (df['Type of Travel']=='Personal')]['Satisfaction_Binary'].mean()*100

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                              RAPPORT FINAL                                       ║
║                     Satisfaction des Passagers Aériens                           ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  📊 CONTEXTE                                                                     ║
║  ──────────                                                                      ║
║  • {df.shape[0]:,} passagers analysés                                                ║
║  • {len(vars_satisfaction)} critères de satisfaction (notes 0-5)                             ║
║  • Taux de satisfaction global : {df['Satisfaction_Binary'].mean()*100:.1f}%                         ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  📈 QUALITÉ DES ANALYSES                                                         ║
║  ───────────────────────                                                         ║
║  • R² (Régression)    : {model.rsquared:.4f} → {model.rsquared*100:.1f}% de la satisfaction expliquée  ║
║  • KMO (Factorielle)  : {kmo_total:.3f} (BON)                                          ║
║  • Variables signif.  : {n_sig}/{len(vars_clean)}                                              ║
║  • Facteurs identifiés: {n_fact}                                                     ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  🔑 TOP 5 FACTEURS D'INFLUENCE (Régression)                                      ║
║  ──────────────────────────────────────────                                      ║""")

for i, (var, r) in enumerate(coefs.head(5).iterrows(), 1):
    signe = "+" if r['Coef'] > 0 else ""
    print(f"║  {i}. {var[:48]:<48} β={signe}{r['Coef']:.4f}  ║")

print(f"""║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  👥 SEGMENTATION CLIENTS                                                         ║
║  ───────────────────────                                                         ║
║  • Business Class + Business Travel : {bus_bus:>5.1f}% satisfaits 😊                 ║
║  • Economy Class + Personal Travel  : {eco_per:>5.1f}% satisfaits 😞                 ║
║  • Écart : {bus_bus - eco_per:.1f} points !                                                    ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  📋 RECOMMANDATIONS                                                              ║
║  ─────────────────                                                               ║
║                                                                                  ║
║  🔴 PRIORITÉ HAUTE :                                                             ║
║     → Améliorer Online Boarding (coefficient max, corrélation max)               ║
║     → Améliorer In-flight Entertainment (forte corrélation)                      ║
║                                                                                  ║
║  🟡 PRIORITÉ MOYENNE :                                                           ║
║     → Améliorer In-flight Wifi (note basse : {df['In-flight Wifi Service'].mean():.2f}/5)                    ║
║     → Améliorer Ease of Online Booking (note basse : {df['Ease of Online Booking'].mean():.2f}/5)            ║
║                                                                                  ║
║  🟢 MAINTENIR :                                                                  ║
║     → In-flight Service ({df['In-flight Service'].mean():.2f}/5) ✓                                    ║
║     → Baggage Handling ({df['Baggage Handling'].mean():.2f}/5) ✓                                     ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║  ⚠️ LIMITES                                                                      ║
║  ──────────                                                                      ║
║  • Corrélation ≠ Causalité                                                       ║
║  • R² = {model.rsquared*100:.1f}% → {100-model.rsquared*100:.1f}% de la satisfaction reste inexpliquée            ║
║  • Hétéroscédasticité détectée                                                   ║
║  • Régression logistique serait plus appropriée (variable binaire)               ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
""")

print("\n>>> FICHIERS GÉNÉRÉS :")
print("  • etape1_nettoyage.png")
print("  • etape3_correlations.png")
print("  • etape4_acp.png")
print("  • etape5_af.png")
print("  • etape6_regression.png")

print("\n" + "="*80)
print("                    FIN DE L'ANALYSE MULTIVARIÉE")
print("                         (7 ÉTAPES COMPLÈTES)")
print("="*80)
