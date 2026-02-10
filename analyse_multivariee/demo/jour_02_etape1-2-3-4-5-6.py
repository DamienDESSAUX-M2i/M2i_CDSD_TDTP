"""
################################################################################
#                                                                              #
#                    PROJET COMPLET : ANALYSE MULTIVARIÉE                      #
#                                                                              #
#                       VERSION ULTRA-DÉTAILLÉE POUR DÉBUTANTS                 #
#                                                                              #
################################################################################

================================================================================
QU'EST-CE QUE CE PROJET ?
================================================================================

Ce projet est un TUTORIEL COMPLET qui vous apprend à analyser des données
en utilisant des techniques statistiques avancées. Chaque ligne de code est
expliquée en détail, comme si vous n'aviez jamais programmé.

CONTEXTE MÉTIER (l'histoire qu'on va étudier) :
-----------------------------------------------
Imaginez que vous êtes le directeur d'une chaîne de restaurants. Vous voulez
comprendre POURQUOI certains clients sont satisfaits et d'autres non.

Vous avez fait remplir un questionnaire à 500 clients qui ont noté différents
aspects de leur expérience (nourriture, service, ambiance...) sur une échelle
de 1 à 10.

VOTRE QUESTION : "Quels sont les facteurs qui influencent le plus la satisfaction ?"

OBJECTIFS DE L'ANALYSE :
------------------------
1. EXPLORER les données (comprendre ce qu'on a)
2. DÉCOUVRIR les dimensions cachées (les "facteurs latents")
3. CONSTRUIRE un modèle pour prédire la satisfaction
4. FAIRE DES RECOMMANDATIONS pour améliorer le restaurant

LES 7 ÉTAPES QU'ON VA SUIVRE :
------------------------------
Étape 1 : Nettoyer les données (supprimer les erreurs)
Étape 2 : Standardiser les variables (les rendre comparables)
Étape 3 : Analyser les corrélations (voir quelles variables vont ensemble)
Étape 4 : ACP - Analyse en Composantes Principales (résumer les données)
Étape 5 : Analyse Factorielle (trouver les dimensions cachées)
Étape 6 : Régression Multiple (construire un modèle prédictif)
Étape 7 : Interpréter et recommander (tirer des conclusions métier)

================================================================================
"""

################################################################################
#                                                                              #
#                              SECTION : IMPORTS                               #
#                                                                              #
################################################################################
"""
QU'EST-CE QU'UN IMPORT ?
========================
En Python, un "import" c'est comme emprunter un outil à une bibliothèque.
Au lieu de tout programmer nous-mêmes, on utilise des outils déjà créés
par d'autres programmeurs.

C'est comme en cuisine : au lieu de fabriquer vous-même votre four,
vous utilisez un four déjà fait par quelqu'un d'autre.
"""

# ------------------------------------------------------------------------------
# IMPORT 1 : NumPy (Numerical Python)
# ------------------------------------------------------------------------------
# NumPy est LA bibliothèque pour faire des calculs mathématiques en Python.
# Elle permet de travailler avec des tableaux de nombres très rapidement.
#
# ANALOGIE : NumPy est comme une calculatrice scientifique super puissante.
#
# Exemples de ce qu'on peut faire avec NumPy :
# - Calculer des moyennes, des écarts-types
# - Générer des nombres aléatoires
# - Faire des opérations sur des matrices
#
# "as np" signifie qu'on donne un surnom à NumPy pour écrire moins.
# Au lieu d'écrire "numpy.mean()", on écrira "np.mean()".

# ------------------------------------------------------------------------------
# IMPORT 9 : Warnings
# ------------------------------------------------------------------------------
# Le module warnings permet de gérer les messages d'avertissement.
# On va désactiver certains avertissements pour avoir un affichage plus propre.
import warnings

# ------------------------------------------------------------------------------
# IMPORT 3 : Matplotlib (pyplot)
# ------------------------------------------------------------------------------
# Matplotlib est LA bibliothèque pour créer des graphiques.
# "pyplot" est le module le plus utilisé de Matplotlib.
#
# ANALOGIE : Matplotlib est comme un logiciel de dessin pour créer des graphiques.
#
# Exemples de ce qu'on peut faire :
# - Histogrammes (barres pour montrer une distribution)
# - Nuages de points (scatter plots)
# - Courbes, camemberts, boxplots, etc.
#
# "as plt" : surnom classique pour pyplot.
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# IMPORT 2 : Pandas
# ------------------------------------------------------------------------------
# Pandas est LA bibliothèque pour manipuler des données sous forme de tableaux.
# Un tableau Pandas s'appelle un "DataFrame" (comme une feuille Excel).
#
# ANALOGIE : Pandas est comme Excel, mais en beaucoup plus puissant.
#
# Exemples de ce qu'on peut faire avec Pandas :
# - Lire des fichiers CSV, Excel
# - Filtrer, trier, grouper des données
# - Calculer des statistiques par groupe
# - Fusionner plusieurs tableaux
#
# "as pd" : surnom pour écrire moins (pd au lieu de pandas).
import pandas as pd

# ------------------------------------------------------------------------------
# IMPORT 4 : Seaborn
# ------------------------------------------------------------------------------
# Seaborn est une bibliothèque de graphiques PLUS JOLIS que Matplotlib.
# Elle est construite au-dessus de Matplotlib et simplifie beaucoup de choses.
#
# ANALOGIE : Si Matplotlib est Paint, Seaborn est Photoshop.
#
# Exemples de ce qu'on peut faire :
# - Heatmaps (cartes de chaleur pour les corrélations)
# - Graphiques statistiques élégants
# - Thèmes visuels prédéfinis
#
# "as sns" : surnom de Seaborn (sns vient du nom du statisticien Samuel Norman Seaborn).
import seaborn as sns

# ------------------------------------------------------------------------------
# IMPORT 8 : Statsmodels
# ------------------------------------------------------------------------------
# Statsmodels est une bibliothèque pour les modèles statistiques classiques.
# C'est comme les logiciels de statistiques professionnels (SPSS, SAS, R).
#
# On importe :
# - sm (statsmodels.api) : fonctions générales
# - smf (formula.api) : pour écrire des formules style R (y ~ x1 + x2)
# - het_breuschpagan : test pour vérifier l'homoscédasticité
# - variance_inflation_factor : pour calculer le VIF (multicolinéarité)
import statsmodels.api as sm

# ------------------------------------------------------------------------------
# IMPORT 7 : Factor Analyzer
# ------------------------------------------------------------------------------
# Cette bibliothèque est spécialisée pour l'Analyse Factorielle.
# Elle n'est pas installée par défaut, il faut l'installer avec :
#     pip install factor_analyzer
#
# On importe :
# - FactorAnalyzer : la classe principale pour faire l'AF
# - calculate_kmo : pour calculer le test KMO
# - calculate_bartlett_sphericity : pour le test de Bartlett
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

# ------------------------------------------------------------------------------
# IMPORT 5 : SciPy (Scientific Python)
# ------------------------------------------------------------------------------
# SciPy est une bibliothèque pour les calculs scientifiques avancés.
# Le module "stats" contient des fonctions statistiques.
#
# On importe plusieurs choses de scipy.stats :
# - zscore : pour standardiser les données
# - shapiro : pour tester si les données suivent une loi normale
# - pearsonr : pour calculer la corrélation de Pearson
# - spearmanr : pour calculer la corrélation de Spearman
from scipy import stats
from scipy.stats import shapiro
from sklearn.decomposition import PCA  # Pour l'ACP

# ------------------------------------------------------------------------------
# IMPORT 6 : Scikit-learn (sklearn)
# ------------------------------------------------------------------------------
# Scikit-learn est LA bibliothèque de Machine Learning en Python.
# Ici, on utilise :
# - StandardScaler : pour standardiser les données (Z-score)
# - PCA : pour l'Analyse en Composantes Principales
from sklearn.preprocessing import StandardScaler  # Pour standardiser
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

import numpy as np

# ------------------------------------------------------------------------------
# CONFIGURATION DE L'ENVIRONNEMENT
# ------------------------------------------------------------------------------
"""
Ces lignes configurent comment Python va se comporter pendant l'exécution.
C'est comme régler les paramètres avant de commencer à travailler.
"""

# Ligne 1 : Définir le style des graphiques
# -----------------------------------------
# plt.style.use() définit un "thème" pour tous les graphiques.
# 'seaborn-v0_8-whitegrid' est un style élégant avec une grille blanche.
# C'est comme choisir un thème dans PowerPoint.

plt.style.use("seaborn-v0_8-whitegrid")

# Ligne 2 : Définir la taille par défaut des graphiques
# -----------------------------------------------------
# plt.rcParams est un dictionnaire qui contient tous les paramètres de Matplotlib.
# 'figure.figsize' définit la taille : (largeur, hauteur) en pouces.
# (12, 6) signifie 12 pouces de large et 6 pouces de haut.

plt.rcParams["figure.figsize"] = (12, 6)

# Ligne 3 : Définir la taille de la police
# ----------------------------------------
# 'font.size' = 10 points. C'est la taille du texte dans les graphiques.

plt.rcParams["font.size"] = 10

# Ligne 4 : Ignorer les avertissements
# ------------------------------------
# Certaines bibliothèques affichent des avertissements qui "polluent" l'écran.
# Cette ligne dit à Python : "ignore tous les avertissements".
# ATTENTION : En production, il vaut mieux les garder pour voir les problèmes.

warnings.filterwarnings("ignore")

# ------------------------------------------------------------------------------
# MESSAGE DE BIENVENUE
# ------------------------------------------------------------------------------
# print() affiche du texte à l'écran.
# "=" * 80 crée une ligne de 80 caractères "=" (répétition).

print("=" * 80)
print("PROJET ANALYSE MULTIVARIÉE - SATISFACTION CLIENT RESTAURANT")
print("=" * 80)


################################################################################
#                                                                              #
#                    SECTION : GÉNÉRATION DES DONNÉES                          #
#                                                                              #
################################################################################
"""
================================================================================
POURQUOI ON GÉNÈRE DES DONNÉES ?
================================================================================

Dans ce tutoriel, on SIMULE des données au lieu d'utiliser de vraies données.

AVANTAGES de la simulation :
1. On CONTRÔLE la structure des données (on sait ce qu'on doit trouver)
2. On peut REPRODUIRE exactement les mêmes résultats
3. Pas de problèmes de confidentialité

COMMENT ON CONSTRUIT LES DONNÉES ?
----------------------------------
On simule 3 "facteurs latents" (concepts cachés qu'on ne mesure pas directement) :
- Facteur "CUISINE" : influence les notes de nourriture
- Facteur "SERVICE" : influence les notes de service
- Facteur "AMBIANCE" : influence les notes d'environnement

Chaque variable observable = Facteur latent + Bruit aléatoire

C'est EXACTEMENT ce que l'Analyse Factorielle va essayer de retrouver !
================================================================================
"""

print("\n" + "=" * 80)
print("GÉNÉRATION DES DONNÉES SIMULÉES")
print("=" * 80)

# ==============================================================================
# ÉTAPE A : Fixer la "graine" aléatoire (random seed)
# ==============================================================================
"""
QU'EST-CE QU'UNE GRAINE ALÉATOIRE (RANDOM SEED) ?
-------------------------------------------------
Les ordinateurs ne peuvent pas vraiment générer des nombres "aléatoires".
Ils utilisent des formules mathématiques qui SIMULENT le hasard.

Le "seed" (graine) est le point de départ de ces formules.
Si on utilise le même seed, on obtient EXACTEMENT les mêmes nombres "aléatoires".

POURQUOI C'EST UTILE ?
- Pour que tout le monde obtienne les mêmes résultats
- Pour pouvoir reproduire une analyse
- Pour débugger (corriger les erreurs)

ANALOGIE : C'est comme noter le numéro d'un tirage de loterie.
Si on refait le tirage avec le même numéro, on obtient les mêmes boules.

np.random.seed(42) :
- np.random : module de NumPy pour les nombres aléatoires
- seed(42) : on choisit 42 comme point de départ
  (42 est une référence geek au "Guide du voyageur galactique")
"""

np.random.seed(42)  # Fixer le hasard pour la reproductibilité

# ==============================================================================
# ÉTAPE B : Définir le nombre d'observations
# ==============================================================================
"""
'n' est une variable qui contient le nombre de clients dans notre enquête.
n = 500 signifie qu'on va simuler les réponses de 500 clients.

POURQUOI 500 ?
- C'est assez pour avoir des résultats statistiquement fiables
- Règle générale : au moins 5 à 10 observations par variable
- Ici on a 11 variables, donc 500 >> 5*11 = 55 (largement suffisant)
"""

n = 500  # Nombre de clients dans notre enquête

print(f"\nNombre de clients simulés : {n}")

# ==============================================================================
# ÉTAPE C : Créer les 3 facteurs latents
# ==============================================================================
"""
QU'EST-CE QU'UN FACTEUR LATENT ?
--------------------------------
Un facteur latent est un CONCEPT CACHÉ qu'on ne peut pas mesurer directement,
mais qui INFLUENCE plusieurs variables observables.

EXEMPLES de facteurs latents dans la vie réelle :
- "Intelligence" : on ne peut pas la mesurer directement, mais elle influence
  les notes en maths, en français, en logique, etc.
- "Santé" : on ne peut pas la mesurer directement, mais elle influence
  la tension, le poids, les analyses sanguines, etc.

DANS NOTRE CAS :
- "Qualité de la cuisine" : influence les notes de nourriture, présentation, fraîcheur
- "Qualité du service" : influence les notes de rapidité, amabilité, compétence
- "Ambiance" : influence les notes de propreté, ambiance, confort

COMMENT ON SIMULE UN FACTEUR LATENT ?
-------------------------------------
On utilise np.random.normal() qui génère des nombres selon une LOI NORMALE.

np.random.normal(moyenne, écart_type, nombre_de_valeurs)

PARAMÈTRES :
- moyenne (μ) : centre de la distribution (valeur la plus fréquente)
- écart_type (σ) : dispersion (plus c'est grand, plus les valeurs sont étalées)
- nombre_de_valeurs : combien de nombres on veut générer

EXEMPLE : np.random.normal(6, 1.5, 500)
- Génère 500 nombres
- Centrés autour de 6
- Avec un écart-type de 1.5
- Environ 68% des valeurs seront entre 4.5 et 7.5 (6 ± 1.5)
- Environ 95% des valeurs seront entre 3 et 9 (6 ± 2*1.5)
"""

print("\n--- Création des facteurs latents ---")

# Facteur 1 : QUALITÉ CUISINE
# ---------------------------
# moyenne = 6 : les clients donnent en moyenne des notes autour de 6
# écart_type = 1.5 : il y a une bonne variabilité dans les opinions
# n = 500 : on génère 500 valeurs (une par client)

facteur_cuisine = np.random.normal(6, 1.5, n)

print(
    f"Facteur CUISINE créé : moyenne={facteur_cuisine.mean():.2f}, écart-type={facteur_cuisine.std():.2f}"
)

# Facteur 2 : QUALITÉ SERVICE
# ---------------------------
# moyenne = 6.5 : les notes de service sont légèrement meilleures que la cuisine
# écart_type = 1.2 : moins de variabilité (le service est plus constant)

facteur_service = np.random.normal(6.5, 1.2, n)

print(
    f"Facteur SERVICE créé : moyenne={facteur_service.mean():.2f}, écart-type={facteur_service.std():.2f}"
)

# Facteur 3 : AMBIANCE
# --------------------
# moyenne = 7 : l'ambiance est généralement bien notée
# écart_type = 1.3 : variabilité intermédiaire

facteur_ambiance = np.random.normal(7, 1.3, n)

print(
    f"Facteur AMBIANCE créé : moyenne={facteur_ambiance.mean():.2f}, écart-type={facteur_ambiance.std():.2f}"
)

# ==============================================================================
# ÉTAPE D : Créer les variables observées
# ==============================================================================
"""
COMMENT ON PASSE DU FACTEUR LATENT À LA VARIABLE OBSERVABLE ?
-------------------------------------------------------------
Chaque variable observable est une COMBINAISON du facteur latent + du bruit.

Formule générale :
    Variable = Facteur × Coefficient + Bruit

- Coefficient : force du lien entre le facteur et la variable (entre 0 et 1)
  - 1.0 = lien parfait
  - 0.9 = lien très fort
  - 0.8 = lien fort
  - etc.

- Bruit : variation aléatoire propre à chaque variable
  - Représente les facteurs spécifiques non capturés par le facteur commun
  - Plus le bruit est grand, moins la variable est liée au facteur

EXEMPLE :
qualite_nourriture = facteur_cuisine × 1.0 + bruit(0, 0.8)
- 1.0 : la qualité de nourriture est PARFAITEMENT liée à la cuisine
- bruit avec écart-type 0.8 : un peu de variation aléatoire

presentation_plats = facteur_cuisine × 0.9 + bruit(0, 1.0)
- 0.9 : la présentation est très liée à la cuisine, mais pas parfaitement
- bruit avec écart-type 1.0 : plus de variation aléatoire
"""

print("\n--- Création des variables observées ---")

# --------------------------------------------------------------------------
# GROUPE 1 : VARIABLES DE CUISINE (influencées par facteur_cuisine)
# --------------------------------------------------------------------------

# Variable 1 : qualite_nourriture
# -------------------------------
# = facteur_cuisine × 1.0 + bruit
# Le coefficient 1.0 signifie que cette variable est la plus représentative du facteur
# Le bruit a un écart-type de 0.8 (assez faible = forte corrélation avec le facteur)

qualite_nourriture = facteur_cuisine * 1.0 + np.random.normal(0, 0.8, n)
#                    ↑                   ↑   ↑
#                    Facteur latent      |   Bruit aléatoire
#                                        |   - moyenne = 0 (pas de biais)
#                    Coefficient = 1.0   |   - écart-type = 0.8
#                    (lien parfait)          - n valeurs

print("  qualite_nourriture : basée sur facteur_cuisine × 1.0 + bruit(σ=0.8)")

# Variable 2 : presentation_plats
# -------------------------------
# Coefficient 0.9 : forte liaison mais pas parfaite
# Bruit σ=1.0 : plus de variation aléatoire

presentation_plats = facteur_cuisine * 0.9 + np.random.normal(0, 1.0, n)

print("  presentation_plats : basée sur facteur_cuisine × 0.9 + bruit(σ=1.0)")

# Variable 3 : fraicheur_ingredients
# ----------------------------------
# Coefficient 0.85 : bonne liaison
# Bruit σ=0.9 : variation modérée

fraicheur_ingredients = facteur_cuisine * 0.85 + np.random.normal(0, 0.9, n)

print("  fraicheur_ingredients : basée sur facteur_cuisine × 0.85 + bruit(σ=0.9)")

# --------------------------------------------------------------------------
# GROUPE 2 : VARIABLES DE SERVICE (influencées par facteur_service)
# --------------------------------------------------------------------------

# Variable 4 : rapidite_service
rapidite_service = facteur_service * 1.0 + np.random.normal(0, 0.7, n)
print("  rapidite_service : basée sur facteur_service × 1.0 + bruit(σ=0.7)")

# Variable 5 : amabilite_personnel
amabilite_personnel = facteur_service * 0.95 + np.random.normal(0, 0.8, n)
print("  amabilite_personnel : basée sur facteur_service × 0.95 + bruit(σ=0.8)")

# Variable 6 : competence_serveur
competence_serveur = facteur_service * 0.9 + np.random.normal(0, 0.9, n)
print("  competence_serveur : basée sur facteur_service × 0.9 + bruit(σ=0.9)")

# --------------------------------------------------------------------------
# GROUPE 3 : VARIABLES D'AMBIANCE (influencées par facteur_ambiance)
# --------------------------------------------------------------------------

# Variable 7 : proprete_restaurant
proprete_restaurant = facteur_ambiance * 1.0 + np.random.normal(0, 0.6, n)
print("  proprete_restaurant : basée sur facteur_ambiance × 1.0 + bruit(σ=0.6)")

# Variable 8 : ambiance
ambiance = facteur_ambiance * 0.9 + np.random.normal(0, 1.0, n)
print("  ambiance : basée sur facteur_ambiance × 0.9 + bruit(σ=1.0)")

# Variable 9 : confort_siege
confort_siege = facteur_ambiance * 0.8 + np.random.normal(0, 1.1, n)
print("  confort_siege : basée sur facteur_ambiance × 0.8 + bruit(σ=1.1)")

# --------------------------------------------------------------------------
# VARIABLE INDÉPENDANTE : rapport_qualite_prix
# --------------------------------------------------------------------------
"""
Cette variable n'est PAS liée aux 3 facteurs principaux.
Elle est INDÉPENDANTE, ce qui nous permettra de voir que l'Analyse Factorielle
la détecte comme différente des autres.
"""

rapport_qualite_prix = np.random.normal(6, 1.5, n)
print("  rapport_qualite_prix : variable INDÉPENDANTE (pas liée aux facteurs)")

# ==============================================================================
# ÉTAPE E : Créer la variable CIBLE (satisfaction_globale)
# ==============================================================================
"""
LA VARIABLE CIBLE (ou variable dépendante) :
--------------------------------------------
C'est la variable qu'on veut PRÉDIRE avec la régression.

Dans notre cas, c'est la satisfaction globale du client.

COMMENT EST-ELLE CALCULÉE ?
La satisfaction est une COMBINAISON PONDÉRÉE des facteurs latents :

satisfaction_globale = 0.40 × facteur_cuisine    (40% d'importance)
                     + 0.35 × facteur_service    (35% d'importance)
                     + 0.15 × facteur_ambiance   (15% d'importance)
                     + 0.10 × rapport_qualite_prix (10% d'importance)
                     + bruit aléatoire

INTERPRÉTATION DES POIDS :
- La cuisine compte le plus (40%)
- Le service est presque aussi important (35%)
- L'ambiance compte moins (15%)
- Le rapport qualité/prix compte un peu (10%)

Le bruit représente tous les autres facteurs qu'on ne mesure pas
(humeur du client, météo, événements personnels, etc.)
"""

print("\n--- Création de la variable cible (satisfaction_globale) ---")

satisfaction_globale = (
    0.40 * facteur_cuisine  # 40% : la cuisine est très importante
    + 0.35 * facteur_service  # 35% : le service aussi
    + 0.15 * facteur_ambiance  # 15% : l'ambiance un peu moins
    + 0.10 * rapport_qualite_prix  # 10% : le rapport qualité/prix un peu
    + np.random.normal(0, 0.5, n)  # Bruit : facteurs non mesurés
)

print(
    "  satisfaction = 0.40×cuisine + 0.35×service + 0.15×ambiance + 0.10×prix + bruit"
)
print(f"  Moyenne de satisfaction : {satisfaction_globale.mean():.2f}")

# ==============================================================================
# ÉTAPE F : Créer le DataFrame (tableau de données)
# ==============================================================================
"""
QU'EST-CE QU'UN DATAFRAME ?
---------------------------
Un DataFrame est un TABLEAU DE DONNÉES, comme une feuille Excel.
- Chaque COLONNE est une variable (ex: qualite_nourriture)
- Chaque LIGNE est une observation (ex: un client)

pd.DataFrame() crée un DataFrame à partir d'un dictionnaire :
- Les CLÉS du dictionnaire deviennent les NOMS des colonnes
- Les VALEURS deviennent les DONNÉES des colonnes

Exemple :
{
    'nom_colonne1': [valeur1, valeur2, valeur3],
    'nom_colonne2': [valeur1, valeur2, valeur3]
}
"""

print("\n--- Création du DataFrame ---")

# Créer le DataFrame
df = pd.DataFrame(
    {
        # Chaque ligne ci-dessous crée une colonne :
        # 'nom_colonne': tableau_de_valeurs
        "qualite_nourriture": qualite_nourriture,  # 500 valeurs
        "presentation_plats": presentation_plats,  # 500 valeurs
        "fraicheur_ingredients": fraicheur_ingredients,  # 500 valeurs
        "rapidite_service": rapidite_service,  # 500 valeurs
        "amabilite_personnel": amabilite_personnel,  # 500 valeurs
        "competence_serveur": competence_serveur,  # 500 valeurs
        "proprete_restaurant": proprete_restaurant,  # 500 valeurs
        "ambiance": ambiance,  # 500 valeurs
        "confort_siege": confort_siege,  # 500 valeurs
        "rapport_qualite_prix": rapport_qualite_prix,  # 500 valeurs
        "satisfaction_globale": satisfaction_globale,  # 500 valeurs (CIBLE)
    }
)

# Afficher les dimensions du DataFrame
print(f"DataFrame créé : {df.shape[0]} lignes × {df.shape[1]} colonnes")
#                          ↑                    ↑
#                          df.shape[0] = nb lignes (500)
#                          df.shape[1] = nb colonnes (11)

# ==============================================================================
# ÉTAPE G : Borner les valeurs entre 1 et 10
# ==============================================================================
"""
POURQUOI BORNER LES VALEURS ?
-----------------------------
Nos notes sont censées être sur une échelle de 1 à 10.
Mais la loi normale peut générer des valeurs HORS de cet intervalle
(par exemple -0.5 ou 12.3).

La méthode .clip(min, max) FORCE les valeurs à rester dans l'intervalle :
- Toute valeur < min devient min
- Toute valeur > max devient max

Exemple :
[0.5, 5, 12] → clip(1, 10) → [1, 5, 10]
"""

print("\n--- Bornage des valeurs entre 1 et 10 ---")

# Boucle FOR : on parcourt chaque colonne du DataFrame
for col in df.columns:
    # Pour chaque colonne, on applique clip(1, 10)
    df[col] = df[col].clip(1, 10)
    #  ↑        ↑          ↑
    #  |        |          clip(min=1, max=10)
    #  |        Sélectionner la colonne 'col'
    #  Remplacer la colonne par sa version bornée

print("✓ Toutes les valeurs sont maintenant entre 1 et 10")

# ==============================================================================
# ÉTAPE H : Ajouter des valeurs manquantes et des outliers (pour l'exercice)
# ==============================================================================
"""
POURQUOI AJOUTER DES PROBLÈMES ?
--------------------------------
Dans la vraie vie, les données sont rarement parfaites. Il y a souvent :
- Des VALEURS MANQUANTES (clients qui n'ont pas répondu à une question)
- Des OUTLIERS (valeurs aberrantes ou extrêmes)

On ajoute ces problèmes pour apprendre à les détecter et les traiter.

SYNTAXE : df.loc[index, colonne] = valeur
- df.loc permet d'accéder à une cellule précise du DataFrame
- index : numéro de la ligne (ici, numéro du client)
- colonne : nom de la colonne
- np.nan : valeur spéciale qui signifie "Not a Number" (valeur manquante)
"""

print("\n--- Ajout de valeurs manquantes et outliers ---")

# Ajouter des valeurs manquantes (NA = Not Available)
df.loc[10, "qualite_nourriture"] = np.nan  # Le client 10 n'a pas répondu
df.loc[25, "rapidite_service"] = np.nan  # Le client 25 n'a pas répondu
df.loc[42, "ambiance"] = np.nan  # Le client 42 n'a pas répondu

print("  3 valeurs manquantes ajoutées (clients 10, 25, 42)")

# Ajouter des valeurs extrêmes (outliers)
df.loc[100, "presentation_plats"] = 1.5  # Note très basse (outlier bas)
df.loc[200, "amabilite_personnel"] = 10.0  # Note maximale (extrême haut)

print("  2 outliers ajoutés (clients 100 et 200)")

# ==============================================================================
# ÉTAPE I : Afficher un aperçu des données
# ==============================================================================
"""
df.head(n) affiche les n PREMIÈRES lignes du DataFrame.
C'est utile pour vérifier que les données sont correctement chargées.

Par défaut, head() affiche 5 lignes. Ici on met 10 pour voir plus.
"""

print("\n--- Aperçu des données (10 premières lignes) ---")
print(df.head(10))
#         ↑
#         Affiche les 10 premières lignes

# Afficher les noms des colonnes
print(f"\nListe des variables : {list(df.columns)}")
#                                  ↑
#                                  df.columns contient les noms des colonnes
#                                  list() le convertit en liste Python

print(f"\n✓ Données générées : {len(df)} clients, {len(df.columns)} variables")
#                              ↑                   ↑
#                              len(df) = nombre de lignes
#                              len(df.columns) = nombre de colonnes


################################################################################
#                                                                              #
#                      ÉTAPE 1 : NETTOYAGE DES DONNÉES                         #
#                                                                              #
################################################################################
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        ÉTAPE 1 : NETTOYAGE DES DONNÉES                       ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  POURQUOI NETTOYER LES DONNÉES ?                                             ║
║  ================================                                            ║
║                                                                              ║
║  "Garbage In, Garbage Out" (ordures en entrée = ordures en sortie)           ║
║                                                                              ║
║  Si vos données contiennent des erreurs, votre analyse sera fausse.          ║
║  C'est comme essayer de construire une maison avec des briques cassées.      ║
║                                                                              ║
║  LES PROBLÈMES COURANTS :                                                    ║
║  ------------------------                                                    ║
║  1. VALEURS MANQUANTES (NA) : Un client n'a pas répondu à une question       ║
║     → Problème : impossible de calculer une moyenne avec des "trous"         ║
║                                                                              ║
║  2. OUTLIERS (valeurs aberrantes) : Un client a mis -999 ou une erreur       ║
║     → Problème : fausse complètement les moyennes et les modèles             ║
║                                                                              ║
║  3. DOUBLONS : La même ligne apparaît plusieurs fois                         ║
║     → Problème : certains clients comptent double dans l'analyse             ║
║                                                                              ║
║  CE QU'ON VA FAIRE :                                                         ║
║  -------------------                                                         ║
║  1.1 Regarder la structure générale des données                              ║
║  1.2 Détecter et traiter les valeurs manquantes                              ║
║  1.3 Détecter les outliers avec la méthode IQR                               ║
║  1.4 Vérifier les doublons                                                   ║
║  1.5 Calculer les statistiques descriptives                                  ║
║  1.6 Visualiser les distributions                                            ║
║                                                                              ║
║  → Ensuite, on pourra passer à l'étape 2 (standardisation)                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n" + "=" * 80)
print("ÉTAPE 1 : NETTOYAGE DES DONNÉES")
print("=" * 80)

# ==============================================================================
# 1.1 INFORMATIONS GÉNÉRALES SUR LE DATASET
# ==============================================================================
"""
Avant de commencer l'analyse, on regarde la "carte d'identité" du DataFrame :
- Combien de lignes ? (observations/clients)
- Combien de colonnes ? (variables)
- Quels types de données ? (nombres, textes, dates...)
"""

print("\n" + "-" * 60)
print("1.1 INFORMATIONS GÉNÉRALES SUR LE DATASET")
print("-" * 60)

# df.shape retourne un TUPLE (nb_lignes, nb_colonnes)
# Un tuple est une paire de valeurs : (500, 11)
# On y accède avec shape[0] (premier élément) et shape[1] (deuxième élément)

print(f"\nDimensions du dataset : {df.shape[0]} lignes × {df.shape[1]} colonnes")
print(f"  → {df.shape[0]} lignes = {df.shape[0]} clients interrogés")
print(f"  → {df.shape[1]} colonnes = {df.shape[1]} questions dans le questionnaire")

# df.dtypes retourne le TYPE de chaque colonne
# float64 = nombre décimal sur 64 bits (ex: 6.5, 7.23)
# int64 = nombre entier sur 64 bits (ex: 1, 2, 3)
# object = texte (chaîne de caractères)

print("\nTypes de données de chaque colonne :")
print(df.dtypes)
print("\n  → float64 signifie 'nombre décimal' (c'est ce qu'on veut pour des notes)")

# ==============================================================================
# 1.2 DÉTECTION ET TRAITEMENT DES VALEURS MANQUANTES (NA)
# ==============================================================================
"""
QU'EST-CE QU'UNE VALEUR MANQUANTE ?
-----------------------------------
Une valeur manquante (NA = Not Available, ou NaN = Not a Number) représente
une donnée ABSENTE. En Python/Pandas, c'est représenté par np.nan.

POURQUOI C'EST UN PROBLÈME ?
- Impossible de calculer une moyenne avec des "trous"
- Beaucoup d'algorithmes refusent de fonctionner avec des NA
- Si on ne les traite pas, ils peuvent propager des erreurs

COMMENT DÉTECTER LES NA ?
-------------------------
df.isnull() crée un DataFrame de booléens (True/False) :
- True si la valeur est manquante
- False si la valeur est présente

df.isnull().sum() compte le nombre de True par colonne.

COMMENT TRAITER LES NA ?
------------------------
Il y a plusieurs options :

1. SUPPRIMER les lignes avec NA : df.dropna()
   + Simple
   - On perd des données

2. IMPUTER (remplacer) par la MOYENNE : df.fillna(df.mean())
   + On garde toutes les données
   - La moyenne est sensible aux outliers

3. IMPUTER par la MÉDIANE : df.fillna(df.median())
   + Robuste aux outliers
   + On garde toutes les données
   - Peut être moins précis si les données sont normales

Ici, on choisit la MÉDIANE car elle est robuste aux outliers.
"""

print("\n" + "-" * 60)
print("1.2 DÉTECTION ET TRAITEMENT DES VALEURS MANQUANTES")
print("-" * 60)

# Étape 1 : Compter les NA par colonne
# ------------------------------------
# df.isnull() : True si NA, False sinon
# .sum() : compte les True (car True=1, False=0)

na_count = df.isnull().sum()
#             ↑         ↑
#             |         Somme des True par colonne
#             DataFrame de booléens

# Nombre total de NA
na_total = na_count.sum()  # Somme de toutes les colonnes

print(f"\nNombre TOTAL de valeurs manquantes : {na_total}")

# Afficher seulement les colonnes qui ONT des NA
# na_count[na_count > 0] : filtre les colonnes avec au moins 1 NA
print("\nDétail par variable (seulement celles avec des NA) :")
print(na_count[na_count > 0])

if na_total == 0:
    print("\n✓ Aucune valeur manquante détectée !")
else:
    print(f"\n⚠️ {na_total} valeurs manquantes à traiter")

# Étape 2 : Imputer les NA par la médiane
# ---------------------------------------
"""
QU'EST-CE QUE LA MÉDIANE ?
--------------------------
La médiane est la valeur qui SÉPARE les données en deux moitiés égales.
Si on range toutes les valeurs par ordre croissant, la médiane est celle du milieu.

EXEMPLE :
Valeurs : [2, 4, 5, 8, 100]
Médiane = 5 (valeur du milieu)
Moyenne = (2+4+5+8+100)/5 = 23.8

Remarquez : la moyenne (23.8) est très différente de la plupart des valeurs
à cause de l'outlier (100). La médiane (5) est plus représentative.

C'est pourquoi on utilise la médiane pour imputer : elle est ROBUSTE aux outliers.

SYNTAXE :
df[col].median() : calcule la médiane de la colonne
df[col].fillna(valeur, inplace=True) : remplace les NA par 'valeur'
  - inplace=True : modifie le DataFrame directement (pas besoin de faire df = ...)
"""

print("\nImputation des valeurs manquantes par la MÉDIANE :")
print("-" * 50)

# Boucle sur toutes les colonnes
for col in df.columns:
    # Vérifier s'il y a des NA dans cette colonne
    nb_na = df[col].isnull().sum()

    if nb_na > 0:
        # Calculer la médiane de la colonne (en ignorant les NA)
        mediane = df[col].median()

        # Remplacer les NA par la médiane
        df[col].fillna(mediane, inplace=True)
        #       ↑               ↑
        #       |               Modifier le DataFrame directement
        #       Remplir les NA avec 'mediane'

        print(f"  '{col}' : {nb_na} NA remplacés par la médiane = {mediane:.2f}")

# Vérification : il ne doit plus y avoir de NA
print(f"\n✓ Après imputation : {df.isnull().sum().sum()} valeurs manquantes")

# ==============================================================================
# 1.3 DÉTECTION DES OUTLIERS AVEC LA MÉTHODE IQR
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      QU'EST-CE QU'UN OUTLIER ?                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Un OUTLIER (ou valeur aberrante) est une valeur TRÈS ÉLOIGNÉE des autres.   ║
║                                                                              ║
║  EXEMPLES dans la vie réelle :                                               ║
║  - Un étudiant de 45 ans dans une classe de licence (moyenne : 20 ans)       ║
║  - Un salaire de 1 million € dans une entreprise (moyenne : 35 000 €)        ║
║  - Une note de 200/20 (erreur de saisie)                                     ║
║                                                                              ║
║  POURQUOI C'EST UN PROBLÈME ?                                                ║
║  - Les outliers FAUSSENT les statistiques (moyenne, écart-type)              ║
║  - Ils peuvent biaiser les modèles de régression                             ║
║  - Ils donnent une image déformée des données                                ║
║                                                                              ║
║  EXEMPLE :                                                                   ║
║  Données : [5, 6, 7, 6, 5, 100]                                              ║
║  Moyenne AVEC le 100 : 21.5 (très différent des valeurs typiques)            ║
║  Moyenne SANS le 100 : 5.8 (plus représentatif)                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                     QU'EST-CE QU'UN QUARTILE ?                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Les QUARTILES divisent les données triées en 4 parties égales.              ║
║                                                                              ║
║  Imaginez que vous rangez 100 élèves par ordre de taille, du plus petit      ║
║  au plus grand :                                                             ║
║                                                                              ║
║  [Plus petits] ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ → [Plus grands]         ║
║                                                                              ║
║       Q1 (25%)      Q2 (50%)      Q3 (75%)                                   ║
║          ↓             ↓             ↓                                       ║
║  [___25%___][___25%___][___25%___][___25%___]                                ║
║                                                                              ║
║  Q1 (1er quartile) : 25% des valeurs sont EN-DESSOUS de Q1                   ║
║  Q2 (2ème quartile) = MÉDIANE : 50% en-dessous, 50% au-dessus                ║
║  Q3 (3ème quartile) : 75% des valeurs sont EN-DESSOUS de Q3                  ║
║                                                                              ║
║  EXEMPLE CONCRET avec des notes : [3, 5, 6, 7, 7, 8, 8, 9, 10]               ║
║  Q1 = 5.5 (entre 5 et 6)                                                     ║
║  Q2 = 7 (la médiane)                                                         ║
║  Q3 = 8.5 (entre 8 et 9)                                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                        MÉTHODE IQR (Interquartile Range)                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  L'IQR est la DIFFÉRENCE entre Q3 et Q1 :                                    ║
║                                                                              ║
║      IQR = Q3 - Q1                                                           ║
║                                                                              ║
║  L'IQR représente l'ÉTENDUE des 50% des valeurs du milieu.                   ║
║  C'est une mesure de DISPERSION robuste aux outliers.                        ║
║                                                                              ║
║  RÈGLE DE TUKEY pour détecter les outliers :                                 ║
║  -------------------------------------------                                 ║
║  Une valeur est un OUTLIER si elle est :                                     ║
║                                                                              ║
║  - EN-DESSOUS de : Q1 - 1.5 × IQR   (outlier BAS)                            ║
║  - AU-DESSUS de  : Q3 + 1.5 × IQR   (outlier HAUT)                           ║
║                                                                              ║
║  POURQUOI 1.5 ?                                                              ║
║  C'est une convention statistique établie par John Tukey.                    ║
║  Avec 1.5, on capture environ 99.3% des données normales.                    ║
║  Donc les outliers sont vraiment exceptionnels.                              ║
║                                                                              ║
║  VISUALISATION :                                                             ║
║                                                                              ║
║  outliers    [─── Q1 ═══════ Q3 ───]    outliers                             ║
║     ↓        ↓                   ↓        ↓                                  ║
║  ●──|──●─────|═══════════════════|─────●──|──●                               ║
║     ↑        ↑                   ↑        ↑                                  ║
║  Q1-1.5×IQR  Q1                  Q3   Q3+1.5×IQR                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n" + "-" * 60)
print("1.3 DÉTECTION DES OUTLIERS (MÉTHODE IQR)")
print("-" * 60)


def detecter_outliers_iqr(serie, nom_variable):
    """
    Détecte les outliers dans une série de données avec la méthode IQR.

    PARAMÈTRES :
    ------------
    serie : pandas.Series
        Une colonne du DataFrame (les valeurs d'une variable)
        Exemple : df['qualite_nourriture'] est une Series

    nom_variable : str
        Le nom de la variable (pour l'affichage)
        Exemple : 'qualite_nourriture'

    RETOURNE :
    ----------
    Un tuple contenant :
    - n_outliers : int, le nombre d'outliers détectés
    - indices : list, les indices (numéros de ligne) des outliers
    - borne_basse : float, la borne en-dessous de laquelle c'est un outlier
    - borne_haute : float, la borne au-dessus de laquelle c'est un outlier

    EXEMPLE D'UTILISATION :
    ----------------------
    n, indices, bb, bh = detecter_outliers_iqr(df['age'], 'age')
    """

    # Étape 1 : Calculer le premier quartile (Q1)
    # -------------------------------------------
    # serie.quantile(0.25) calcule la valeur en-dessous de laquelle
    # se trouvent 25% des données.
    #
    # quantile(x) avec x entre 0 et 1 :
    # - quantile(0.25) = Q1 (premier quartile)
    # - quantile(0.50) = médiane
    # - quantile(0.75) = Q3 (troisième quartile)

    Q1 = serie.quantile(0.25)
    #          ↑
    #          0.25 = 25% = premier quartile

    # Étape 2 : Calculer le troisième quartile (Q3)
    # ---------------------------------------------
    # 75% des données sont en-dessous de Q3

    Q3 = serie.quantile(0.75)
    #          ↑
    #          0.75 = 75% = troisième quartile

    # Étape 3 : Calculer l'IQR (Interquartile Range)
    # ----------------------------------------------
    # IQR = écart entre Q3 et Q1
    # C'est l'étendue des 50% des données du milieu

    IQR = Q3 - Q1

    # Étape 4 : Calculer les bornes
    # -----------------------------
    # Tout ce qui est en-dehors de ces bornes est un outlier

    borne_basse = Q1 - 1.5 * IQR  # Seuil pour les outliers bas
    borne_haute = Q3 + 1.5 * IQR  # Seuil pour les outliers hauts

    # Étape 5 : Identifier les outliers
    # ---------------------------------
    # On crée un masque booléen (True/False) pour chaque valeur :
    # True si la valeur est un outlier, False sinon

    outliers = (serie < borne_basse) | (serie > borne_haute)
    #           ↑                       ↑
    #           Condition 1 : trop bas  Condition 2 : trop haut
    #                        ↑
    #                        | = OU logique
    #                        Une valeur est outlier si l'une des deux conditions est vraie

    # Étape 6 : Compter les outliers
    # ------------------------------
    # .sum() compte les True (True = 1, False = 0)

    n_outliers = outliers.sum()

    # Étape 7 : Récupérer les indices des outliers
    # --------------------------------------------
    # serie[outliers] : sélectionne seulement les outliers
    # .index : récupère les indices (numéros de ligne)
    # .tolist() : convertit en liste Python

    indices_outliers = serie[outliers].index.tolist()

    return n_outliers, indices_outliers, borne_basse, borne_haute


# Appliquer la détection à toutes les colonnes
# --------------------------------------------

print("\nRésumé des outliers par variable :")
print("-" * 70)
print(f"{'Variable':<30} | {'Outliers':>8} | {'Borne basse':>12} | {'Borne haute':>12}")
print("-" * 70)

outliers_total = 0  # Compteur total

# Boucle sur toutes les colonnes du DataFrame
for col in df.columns:
    # Appeler notre fonction pour cette colonne
    n_out, indices, bb, bh = detecter_outliers_iqr(df[col], col)

    # Additionner au total
    outliers_total += n_out

    # Afficher seulement si on a trouvé des outliers
    if n_out > 0:
        print(f"{col:<30} | {n_out:>8} | {bb:>12.2f} | {bh:>12.2f}")

print("-" * 70)
print(f"{'TOTAL':<30} | {outliers_total:>8} |")
print("-" * 70)

# Décision sur les outliers
# -------------------------
"""
QUE FAIRE DES OUTLIERS ?

Option 1 : Les SUPPRIMER
- Si ce sont des erreurs de saisie
- Si ils déforment trop l'analyse
- ATTENTION : on perd des données

Option 2 : Les CONSERVER
- Si ce sont des valeurs légitimes (vraies observations)
- Si ils représentent des cas intéressants

Option 3 : Les REMPLACER (winsorisation)
- Remplacer par les bornes (outlier → borne)
- Conserve le nombre de données

ICI, on choisit de CONSERVER les outliers car :
- Nos données sont des notes de 1 à 10 (plage limitée)
- Les outliers sont modérés (pas de valeurs absurdes)
- Ils peuvent représenter des opinions extrêmes mais légitimes
"""

print(f"\n✓ {outliers_total} outliers détectés - CONSERVÉS (valeurs modérées)")
print("  → Les valeurs sont dans la plage 1-10, donc légitimes")

# ==============================================================================
# 1.4 VÉRIFICATION DES DOUBLONS
# ==============================================================================
"""
QU'EST-CE QU'UN DOUBLON ?
-------------------------
Un doublon est une ligne qui apparaît PLUSIEURS FOIS dans le DataFrame.
C'est souvent une erreur (même client enregistré deux fois).

POURQUOI C'EST UN PROBLÈME ?
- Certains clients "comptent double" dans l'analyse
- Fausse les statistiques et les proportions
- Peut biaiser les modèles

df.duplicated() retourne True pour chaque ligne qui est une copie
d'une ligne précédente.
"""

print("\n" + "-" * 60)
print("1.4 VÉRIFICATION DES DOUBLONS")
print("-" * 60)

# Compter les doublons
# df.duplicated() : True si la ligne est un doublon
# .sum() : compte les True

n_doublons = df.duplicated().sum()
#              ↑              ↑
#              |              Compte les lignes dupliquées
#              Identifie les doublons (True/False)

print(f"\nNombre de lignes dupliquées : {n_doublons}")

if n_doublons > 0:
    # Supprimer les doublons
    # drop_duplicates() garde la première occurrence et supprime les copies
    df = df.drop_duplicates()
    print(f"✓ Doublons supprimés - Nouveau nombre de lignes : {len(df)}")
else:
    print("✓ Aucun doublon détecté")

# ==============================================================================
# 1.5 STATISTIQUES DESCRIPTIVES
# ==============================================================================
"""
QU'EST-CE QUE LES STATISTIQUES DESCRIPTIVES ?
---------------------------------------------
Ce sont des résumés numériques qui décrivent les données :
- TENDANCE CENTRALE : où se situe le "centre" des données
- DISPERSION : comment les données sont étalées
- FORME : symétrie, aplatissement

df.describe() calcule automatiquement les statistiques principales :

- count : nombre de valeurs (non manquantes)
- mean : moyenne arithmétique (somme / nombre)
- std : écart-type (mesure de dispersion)
- min : valeur minimum
- 25% : premier quartile (Q1)
- 50% : médiane (Q2)
- 75% : troisième quartile (Q3)
- max : valeur maximum
"""

print("\n" + "-" * 60)
print("1.5 STATISTIQUES DESCRIPTIVES (après nettoyage)")
print("-" * 60)

# Calculer et afficher les statistiques
# .round(2) arrondit à 2 décimales pour la lisibilité

print("\n" + df.describe().round(2).to_string())
#            ↑          ↑         ↑
#            |          |         Convertir en string pour un bel affichage
#            |          Arrondir à 2 décimales
#            Calculer toutes les statistiques

# Interprétation des statistiques
print("\n--- Comment lire ce tableau ? ---")
print("""
  • count : nombre de réponses (500 pour toutes = pas de NA)
  • mean : note moyenne (autour de 6-7 pour toutes les variables)
  • std : écart-type (environ 1.5-2 = variabilité modérée)
  • min : note minimum (entre 1 et 3)
  • 25% : Q1, premier quartile (25% des notes sont en-dessous)
  • 50% : médiane (la moitié des clients ont noté en-dessous)
  • 75% : Q3, troisième quartile (75% des notes sont en-dessous)
  • max : note maximum (entre 9 et 10)
""")

# ==============================================================================
# 1.6 VISUALISATION DES DISTRIBUTIONS
# ==============================================================================
"""
QU'EST-CE QU'UNE DISTRIBUTION ?
-------------------------------
La distribution montre COMMENT les valeurs sont réparties.
- Beaucoup de valeurs au centre ? (distribution normale)
- Plus de petites valeurs ? (asymétrie à gauche)
- Plus de grandes valeurs ? (asymétrie à droite)

HISTOGRAMME :
Un graphique en barres qui montre la fréquence de chaque intervalle de valeurs.
Plus une barre est haute, plus il y a de valeurs dans cet intervalle.

plt.subplots(lignes, colonnes) crée une grille de graphiques.
Par exemple : plt.subplots(3, 4) crée une grille de 3 lignes × 4 colonnes = 12 graphiques.
"""

print("\n" + "-" * 60)
print("1.6 VISUALISATION DES DISTRIBUTIONS")
print("-" * 60)

# Créer une grille de 3 lignes × 4 colonnes = 12 espaces pour graphiques
# figsize=(16, 10) : taille de la figure (16 pouces de large, 10 de haut)

fig, axes = plt.subplots(3, 4, figsize=(16, 10))
#   ↑   ↑           ↑
#   |   |           Taille de la figure
#   |   Liste des "axes" (espaces pour les graphiques)
#   La figure complète

# axes est un tableau 2D (3×4). On le "aplatit" en liste 1D pour faciliter la boucle
axes = axes.flatten()
#           ↑
#           Transformer [[ax1,ax2,ax3,ax4], [ax5,ax6,ax7,ax8], [ax9,ax10,ax11,ax12]]
#           en [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12]

# Boucle sur chaque colonne du DataFrame
# enumerate() donne à la fois l'index (i) et la valeur (col)
for i, col in enumerate(df.columns):
    ax = axes[i]  # Sélectionner le graphique numéro i

    # Créer l'histogramme
    ax.hist(
        df[col],  # Les données à afficher
        bins=20,  # Nombre de barres (bins = "bacs")
        edgecolor="white",  # Couleur des bords des barres
        alpha=0.7,  # Transparence (0=invisible, 1=opaque)
        color="steelblue",  # Couleur des barres
    )

    # Ajouter une ligne verticale pour la moyenne
    ax.axvline(
        df[col].mean(),  # Position : la moyenne
        color="red",  # Couleur rouge
        linestyle="--",  # Style pointillé
        label=f"Moy={df[col].mean():.1f}",  # Étiquette pour la légende
    )

    # Ajouter une ligne verticale pour la médiane
    ax.axvline(
        df[col].median(),  # Position : la médiane
        color="green",  # Couleur verte
        linestyle="--",  # Style pointillé
        label=f"Méd={df[col].median():.1f}",
    )

    ax.set_title(col, fontsize=9)  # Titre du graphique
    ax.legend(fontsize=7)  # Afficher la légende

# Le dernier espace (12) est vide car on a 11 variables
axes[-1].axis("off")  # Masquer le dernier graphique

# Titre principal de la figure
plt.suptitle(
    "ÉTAPE 1 : Distribution des variables après nettoyage",
    fontsize=14,
    fontweight="bold",
)

# Ajuster l'espacement entre les graphiques
plt.tight_layout()

# Sauvegarder la figure
plt.savefig("etape1_distributions.png", dpi=150, bbox_inches="tight")
plt.close()  # Fermer la figure (libérer la mémoire)

print("✓ Graphique sauvegardé : etape1_distributions.png")

# ==============================================================================
# BILAN DE L'ÉTAPE 1
# ==============================================================================

print("\n" + "=" * 80)
print("BILAN DE L'ÉTAPE 1 : NETTOYAGE DES DONNÉES")
print("=" * 80)
print(f"""
RÉSUMÉ :
--------
✓ Valeurs manquantes traitées : {na_total} → 0 (imputation par la médiane)
✓ Outliers détectés : {outliers_total} (conservés car modérés)
✓ Doublons supprimés : {n_doublons}
✓ Dataset final : {len(df)} observations × {len(df.columns)} variables

POURQUOI PASSER À L'ÉTAPE 2 MAINTENANT ?
----------------------------------------
Les données sont maintenant PROPRES :
- Pas de trous (NA)
- Pas de valeurs impossibles
- Pas de doublons

On peut maintenant les STANDARDISER pour qu'elles soient comparables.
""")

################################################################################
#                    ÉTAPE 2 : STANDARDISATION                                 #
################################################################################

print("\n" + "=" * 80)
print("ÉTAPE 2 : STANDARDISATION")
print("=" * 80)

# 2.1 Séparation X et Y
print("\n--- 2.1 Séparation X (explicatives) et Y (cible) ---")

variables_X = [col for col in df.columns if col != "satisfaction_globale"]
variable_Y = "satisfaction_globale"

X = df[variables_X].copy()
y = df[variable_Y].copy()

print(f"  X = {len(variables_X)} variables explicatives")
print(f"  Y = {variable_Y}")

# ══════════════════════════════════════════════════════════════════════════════
# VÉRIFICATION AVANT STANDARDISATION
# ══════════════════════════════════════════════════════════════════════════════

print("\n--- Vérification avant standardisation ---")
print(f"  NaN dans X : {X.isnull().sum().sum()}")

if X.isnull().sum().sum() > 0:
    print("  ⚠️ Traitement des NaN restants...")
    for col in X.columns:
        X[col] = X[col].fillna(X[col].median())

# 2.2 Standardisation
print("\n--- 2.2 Application de la standardisation ---")

scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

# ══════════════════════════════════════════════════════════════════════════════
# VÉRIFICATION APRÈS STANDARDISATION
# ══════════════════════════════════════════════════════════════════════════════

print("\n--- Vérification après standardisation ---")
na_in_scaled = X_scaled.isnull().sum().sum()
print(f"  NaN dans X_scaled : {na_in_scaled}")

if na_in_scaled > 0:
    print("  ❌ ERREUR : X_scaled contient des NaN !")
    X_scaled = X_scaled.fillna(0)
else:
    print("  ✓ X_scaled est propre, l'ACP peut fonctionner")

print("""
  ═══════════════════════════════════════════════════════════════════════════
  BILAN ÉTAPE 2 : Variables standardisées ✓
  → Moyennes ≈ 0, Écarts-types ≈ 1
  ═══════════════════════════════════════════════════════════════════════════
""")


################################################################################
#                    ÉTAPE 3 : CORRÉLATIONS                                    #
################################################################################

print("\n" + "=" * 80)
print("ÉTAPE 3 : ANALYSE DES CORRÉLATIONS")
print("=" * 80)

# 3.1 Matrice de corrélation
print("\n--- 3.1 Matrice de corrélation ---")
corr_matrix = X.corr(method="pearson")
print("  ✓ Matrice calculée")

# 3.2 Corrélations fortes
print("\n--- 3.2 Corrélations fortes (|r| ≥ 0.5) ---")

correlations_fortes = []
cols = corr_matrix.columns
for i in range(len(cols)):
    for j in range(i + 1, len(cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) >= 0.5:
            correlations_fortes.append(
                {
                    "Variable_1": cols[i],
                    "Variable_2": cols[j],
                    "Corrélation": round(r, 3),
                }
            )

correlations_fortes_df = pd.DataFrame(correlations_fortes)
if len(correlations_fortes_df) > 0:
    correlations_fortes_df = correlations_fortes_df.sort_values(
        "Corrélation", key=abs, ascending=False
    )
    print(correlations_fortes_df.to_string(index=False))

# 3.3 Corrélations avec Y
print("\n--- 3.3 Corrélations avec satisfaction_globale ---")

df_complet = df[variables_X + [variable_Y]]
matrice_complete = df_complet.corr()
corr_avec_y = matrice_complete[variable_Y].drop(variable_Y)
corr_avec_y_sorted = corr_avec_y.abs().sort_values(ascending=False)

print("\nClassement par impact sur la satisfaction :")
for var in corr_avec_y_sorted.index:
    r = corr_avec_y[var]
    print(f"  {var:30} : r = {r:+.3f}")

# 3.4 Visualisation
print("\n--- 3.4 Visualisation ---")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=axes[0]
)
axes[0].set_title("Matrice de corrélation", fontweight="bold")

valeurs_triees = corr_avec_y.loc[corr_avec_y_sorted.index]
colors = ["green" if x > 0 else "red" for x in valeurs_triees]
valeurs_triees.plot(kind="barh", ax=axes[1], color=colors)
axes[1].axvline(x=0, color="black", linewidth=0.5)
axes[1].set_title("Corrélation avec satisfaction", fontweight="bold")

plt.tight_layout()
plt.savefig("etape3_correlations.png", dpi=150)
plt.close()

print("  ✓ Graphique sauvegardé : etape3_correlations.png")

print(f"""
  ═══════════════════════════════════════════════════════════════════════════
  BILAN ÉTAPE 3 : {len(correlations_fortes)} paires fortement corrélées ✓
  → Variable la plus liée à la satisfaction : {corr_avec_y_sorted.index[0]}
  ═══════════════════════════════════════════════════════════════════════════
""")


################################################################################
#                    ÉTAPE 4 : ACP                                             #
################################################################################
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       QU'EST-CE QUE L'ACP ?                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🎯 OBJECTIF : Savoir COMBIEN de "dimensions cachées" il y a.                ║
║                                                                              ║
║  📸 ANALOGIE : Prendre une photo 2D d'une statue 3D.                         ║
║  L'ACP trouve les meilleurs ANGLES pour capturer le maximum d'info.          ║
║                                                                              ║
║  📊 CE QU'ON CHERCHE :                                                       ║
║  → Combien de COMPOSANTES PRINCIPALES garder ?                               ║
║  → On utilise la RÈGLE DE KAISER : garder celles avec valeur propre > 1      ║
║                                                                              ║
║  🔗 LIEN AVEC L'ÉTAPE 5 :                                                    ║
║  Le nombre de composantes de l'ACP = le nombre de FACTEURS de l'AF !         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n" + "=" * 80)
print("ÉTAPE 4 : ANALYSE EN COMPOSANTES PRINCIPALES (ACP)")
print("=" * 80)

# ══════════════════════════════════════════════════════════════════════════════
# VÉRIFICATION CRITIQUE AVANT L'ACP (évite l'erreur "Input X contains NaN")
# ══════════════════════════════════════════════════════════════════════════════

print("\n--- Vérification AVANT l'ACP ---")
print(f"  Dimensions de X_scaled : {X_scaled.shape}")
print(f"  NaN dans X_scaled : {X_scaled.isnull().sum().sum()}")

if X_scaled.isnull().sum().sum() > 0:
    print("  ⚠️ NaN détectés ! Traitement d'urgence...")
    X_scaled = X_scaled.fillna(0)
    print(f"  ✓ NaN traités. Nouveau compte : {X_scaled.isnull().sum().sum()}")
else:
    print("  ✓ Pas de NaN, l'ACP peut fonctionner")

# 4.1 Création et ajustement de l'ACP
print("\n--- 4.1 Création et ajustement de l'ACP ---")

pca = PCA()

try:
    pca.fit(X_scaled)
    print("  ✓ ACP calculée avec succès")
except ValueError as e:
    print(f"  ❌ ERREUR : {e}")
    raise

# 4.2 Extraction des résultats
print("\n--- 4.2 Variance expliquée par composante ---")

variance_expliquee = pca.explained_variance_ratio_
variance_cumulee = variance_expliquee.cumsum()
valeurs_propres = pca.explained_variance_

print("-" * 70)
print(f"{'Composante':<12} | {'Variance':<12} | {'Cumulée':<12} | {'λ':>6} | Kaiser")
print("-" * 70)

for i, (v, c, lam) in enumerate(
    zip(variance_expliquee, variance_cumulee, valeurs_propres)
):
    kaiser = "← λ>1 !" if lam > 1 else ""
    barre = "█" * int(v * 40)
    print(
        f"PC{i + 1:<10} | {v * 100:>10.1f}% | {c * 100:>10.1f}% | {lam:>5.2f} | {kaiser}"
    )

print("-" * 70)

# 4.3 Choix du nombre de composantes
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║            COMBIEN DE COMPOSANTES GARDER ?                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1️⃣ RÈGLE DES 80% :                                                          ║
║     "Garder assez de composantes pour expliquer ≥80% de la variance"         ║
║                                                                              ║
║  2️⃣ RÈGLE DE KAISER :                                                        ║
║     "Garder les composantes avec valeur propre (λ) > 1"                      ║
║                                                                              ║
║  👉 POURQUOI λ > 1 ?                                                         ║
║     Après standardisation, chaque variable a une variance de 1.              ║
║     Une composante avec λ > 1 explique PLUS qu'une variable seule.           ║
║     Si λ < 1, autant garder les variables originales !                       ║
║                                                                              ║
║  🔗 CE NOMBRE EST CRUCIAL :                                                  ║
║     C'est lui qu'on utilisera pour l'Analyse Factorielle à l'étape 5 !       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- 4.3 Choix du nombre de composantes ---")

# Règle des 80%
n_80pct = (variance_cumulee >= 0.80).argmax() + 1

# Règle de Kaiser
n_kaiser = sum(valeurs_propres > 1)

print(f"\n  1️⃣ RÈGLE DES 80% : {n_80pct} composantes pour ≥80% de variance")
print(f"  2️⃣ RÈGLE DE KAISER : {n_kaiser} composantes avec λ > 1")

n_composantes = max(n_80pct, n_kaiser)
print(
    f"\n  >>> DÉCISION : {n_composantes} composantes ({variance_cumulee[n_composantes - 1] * 100:.1f}% de variance)"
)

# 4.4 Visualisation
print("\n--- 4.4 Visualisation (Scree Plot) ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

x = range(1, len(valeurs_propres) + 1)
axes[0].bar(
    x, variance_expliquee * 100, alpha=0.6, color="steelblue", label="Individuelle"
)
axes[0].plot(x, variance_cumulee * 100, "ro-", label="Cumulée")
axes[0].axhline(80, color="green", linestyle="--", label="Seuil 80%")
axes[0].set_xlabel("Composante")
axes[0].set_ylabel("Variance (%)")
axes[0].set_title("Scree Plot", fontweight="bold")
axes[0].legend()

colors = ["green" if lam > 1 else "gray" for lam in valeurs_propres]
axes[1].bar(x, valeurs_propres, color=colors)
axes[1].axhline(1, color="red", linestyle="--", linewidth=2, label="Seuil Kaiser (λ=1)")
axes[1].set_xlabel("Composante")
axes[1].set_ylabel("Valeur propre (λ)")
axes[1].set_title("Critère de Kaiser", fontweight="bold")
axes[1].legend()

plt.tight_layout()
plt.savefig("etape4_acp.png", dpi=150)
plt.close()

print("  ✓ Graphique sauvegardé : etape4_acp.png")

print(f"""
  ═══════════════════════════════════════════════════════════════════════════
  BILAN ÉTAPE 4 : ACP ✓
  
  ✓ {n_kaiser} composantes avec valeur propre > 1 (critère de Kaiser)
  ✓ {n_80pct} composantes pour atteindre 80% de variance
  ✓ DÉCISION : {n_composantes} composantes ({variance_cumulee[n_composantes - 1] * 100:.1f}%)
  
  🔗 LIEN AVEC L'ÉTAPE 5 :
  ─────────────────────────
  Ce nombre ({n_composantes}) sera utilisé comme nombre de FACTEURS dans l'AF.
  
  L'ACP dit COMBIEN de dimensions → {n_composantes}
  L'AF va dire QUELLES SONT ces dimensions (Cuisine, Service, Ambiance)
  ═══════════════════════════════════════════════════════════════════════════
""")


################################################################################
#                    ÉTAPE 5 : ANALYSE FACTORIELLE                             #
################################################################################
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QU'EST-CE QUE L'ANALYSE FACTORIELLE ?                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🎯 OBJECTIF : Découvrir les "THÈMES CACHÉS" qui expliquent nos données.     ║
║                                                                              ║
║  🎓 ANALOGIE DE L'ÉCOLE :                                                    ║
║  ─────────────────────────                                                   ║
║  Un élève a ces notes : Maths=15, Physique=14, Chimie=16, Français=10        ║
║                                                                              ║
║  Tu remarques que Maths, Physique et Chimie sont CORRÉLÉES.                  ║
║  POURQUOI ? Parce qu'il existe une "APTITUDE CACHÉE" :                       ║
║  → L'aptitude SCIENTIFIQUE influence les 3 notes !                           ║
║                                                                              ║
║  Cette aptitude n'est pas mesurée directement.                               ║
║  L'Analyse Factorielle la DÉCOUVRE à partir des corrélations.                ║
║                                                                              ║
║  🍽️ DANS NOTRE CAS :                                                         ║
║  ────────────────────                                                        ║
║  - Facteur 1 = "QUALITÉ CUISINE" → influence qualite, presentation, fraicheur║
║  - Facteur 2 = "QUALITÉ SERVICE" → influence rapidite, amabilite, competence ║
║  - Facteur 3 = "AMBIANCE" → influence proprete, ambiance, confort            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n" + "=" * 80)
print("ÉTAPE 5 : ANALYSE FACTORIELLE")
print("=" * 80)


# ==============================================================================
# 5.1 TEST KMO
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        QU'EST-CE QUE LE KMO ?                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Le KMO est une NOTE DE 0 à 1 qui répond à :                                 ║
║  "Est-ce que mes variables partagent quelque chose en commun ?"              ║
║                                                                              ║
║  🍕 ANALOGIE DE LA PIZZA :                                                   ║
║  ─────────────────────────                                                   ║
║  Tu commandes une pizza pour 10 amis.                                        ║
║                                                                              ║
║  • KMO ÉLEVÉ (≥ 0.8) = Tous aiment les mêmes garnitures                      ║
║    → Facile de commander UNE pizza qui plaît à tous !                        ║
║    → Les variables "vont bien ensemble" ✓                                    ║
║                                                                              ║
║  • KMO FAIBLE (< 0.6) = Chacun veut des garnitures différentes               ║
║    → Impossible de trouver une pizza universelle                             ║
║    → Les variables sont trop différentes ✗                                   ║
║                                                                              ║
║  📏 GRILLE DE LECTURE :                                                      ║
║     KMO ≥ 0.9  →  EXCELLENT 😍                                               ║
║     KMO ≥ 0.8  →  TRÈS BON 😊                                                ║
║     KMO ≥ 0.7  →  BON 🙂                                                     ║
║     KMO < 0.6  →  MAUVAIS 😞 (Stop, ne fais pas l'AF)                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- 5.1 Test KMO : 'Mes données sont-elles adaptées ?' ---")

kmo_per_variable, kmo_total = calculate_kmo(X)

print(f"\n  KMO global : {kmo_total:.3f}")

if kmo_total >= 0.9:
    interpretation_kmo = "EXCELLENT 😍"
elif kmo_total >= 0.8:
    interpretation_kmo = "TRÈS BON 😊"
elif kmo_total >= 0.7:
    interpretation_kmo = "BON 🙂"
else:
    interpretation_kmo = "INSUFFISANT 😞"

print(f"  Interprétation : {interpretation_kmo}")

if kmo_total >= 0.7:
    print("\n  ✓ KMO ≥ 0.7 → L'Analyse Factorielle EST appropriée")
else:
    print("\n  ⚠️ KMO < 0.7 → L'Analyse Factorielle n'est PAS recommandée")


# ==============================================================================
# 5.2 TEST DE BARTLETT
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     QU'EST-CE QUE LE TEST DE BARTLETT ?                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Ce test répond à :                                                          ║
║  "Est-ce que mes variables sont VRAIMENT liées entre elles ?"                ║
║                                                                              ║
║  🎲 ANALOGIE DU GROUPE D'AMIS :                                              ║
║  ──────────────────────────────                                              ║
║                                                                              ║
║  • SI BARTLETT DIT "OUI" (p < 0.05) :                                        ║
║    Quand Pierre est content, Marie l'est aussi.                              ║
║    → Ces personnes sont CONNECTÉES                                           ║
║    → On peut chercher ce qui les lie (= les facteurs) ✓                      ║
║                                                                              ║
║  • SI BARTLETT DIT "NON" (p ≥ 0.05) :                                        ║
║    L'humeur de chacun n'a rien à voir avec les autres.                       ║
║    → Ces personnes sont INDÉPENDANTES                                        ║
║    → Inutile de chercher des facteurs communs ✗                              ║
║                                                                              ║
║  ⚠️ ATTENTION : Ici, PETIT = BON !                                           ║
║     p = 0.00001 → EXCELLENT                                                  ║
║     p = 0.50 → MAUVAIS                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- 5.2 Test de Bartlett : 'Mes variables sont-elles liées ?' ---")

chi2, p_bartlett = calculate_bartlett_sphericity(X)

print(f"\n  Chi² = {chi2:.0f}")
print(f"  p-value = {p_bartlett:.2e}")

if p_bartlett < 0.05:
    print("\n  ✓ p < 0.05 → Variables corrélées → AF justifiée")
else:
    print("\n  ⚠️ p ≥ 0.05 → Variables indépendantes → AF non justifiée")


# ==============================================================================
# 5.3 D'OÙ VIENNENT LES FACTEURS ? POURQUOI CE NOMBRE ?
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    D'OÙ VIENNENT LES FACTEURS ?                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🤔 QUESTION 1 : D'où viennent Facteur1, Facteur2, Facteur3 ?                ║
║  ─────────────────────────────────────────────────────────────               ║
║                                                                              ║
║  Les facteurs sont des "VARIABLES CACHÉES" que l'algorithme INVENTE          ║
║  pour expliquer les corrélations entre nos variables.                        ║
║                                                                              ║
║  L'algorithme observe que :                                                  ║
║  - qualite_nourriture, presentation, fraicheur sont TRÈS corrélées           ║
║  - rapidite_service, amabilite, competence sont TRÈS corrélées               ║
║  - proprete, ambiance, confort sont TRÈS corrélées                           ║
║                                                                              ║
║  Il se dit : "Il doit exister QUELQUE CHOSE qui fait qu'elles bougent        ║
║               ensemble. Je vais INVENTER une variable cachée pour            ║
║               expliquer ça."                                                 ║
║                                                                              ║
║  Ces "quelque chose" = les FACTEURS !                                        ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🤔 QUESTION 2 : Ça représente quoi ?                                        ║
║  ────────────────────────────────────                                        ║
║                                                                              ║
║  Au départ, Facteur1, Facteur2, Facteur3 sont juste des NUMÉROS !            ║
║  L'algorithme ne sait pas ce qu'ils signifient.                              ║
║                                                                              ║
║  C'est NOUS (les humains) qui regardons les loadings et disons :             ║
║  - "Facteur 1 contient nourriture, présentation, fraîcheur... Ah !           ║
║     C'est la CUISINE !"                                                      ║
║                                                                              ║
║  Le NOM est une INTERPRÉTATION HUMAINE, pas un calcul automatique.           ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🤔 QUESTION 3 : POURQUOI CE NOMBRE de facteurs ?                            ║
║  ────────────────────────────────────────────────                            ║
║                                                                              ║
║  Le nombre vient DIRECTEMENT de l'ÉTAPE 4 (ACP) !                            ║
║                                                                              ║
║  L'ACP a calculé les VALEURS PROPRES (λ) :                                   ║
║  ┌─────┬────────────┬─────────────┐                                          ║
║  │ PC  │ Val.propre │ Garder ?    │                                          ║
║  ├─────┼────────────┼─────────────┤                                          ║
║  │ PC1 │    3.2     │ ✓ OUI (>1)  │                                          ║
║  │ PC2 │    2.1     │ ✓ OUI (>1)  │                                          ║
║  │ PC3 │    1.4     │ ✓ OUI (>1)  │                                          ║
║  │ PC4 │    0.8     │ ✗ NON (<1)  │                                          ║
║  └─────┴────────────┴─────────────┘                                          ║
║                                                                              ║
║  RÈGLE DE KAISER : On garde les composantes avec λ > 1                       ║
║  → 3 composantes ont λ > 1 → On extrait 3 FACTEURS                           ║
║                                                                              ║
║  👉 n_facteurs = n_kaiser (résultat de l'ACP)                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- 5.3 Création du modèle factoriel ---")

# Le nombre de facteurs vient de l'ACP (critère de Kaiser)
n_facteurs = n_kaiser  # ← LIEN DIRECT AVEC L'ACP !

print(f"""
  ╔════════════════════════════════════════════════════════════════════════╗
  ║  🔗 LIEN ACP → ANALYSE FACTORIELLE                                     ║
  ╠════════════════════════════════════════════════════════════════════════╣
  ║                                                                        ║
  ║  L'ACP (étape 4) a trouvé : {n_kaiser} composantes avec valeur propre > 1    ║
  ║                                                                        ║
  ║  DONC : On extrait {n_facteurs} FACTEURS dans l'Analyse Factorielle          ║
  ║                                                                        ║
  ║  L'ACP dit COMBIEN de dimensions ? → {n_kaiser}                              ║
  ║  L'AF dit QUELLES SONT ces dimensions ? → (on va le découvrir)         ║
  ║                                                                        ║
  ╚════════════════════════════════════════════════════════════════════════╝
""")

# Créer et ajuster le modèle
# NOTE : Si vous avez une erreur "force_all_finite", mettez à jour factor_analyzer :
#        pip install --upgrade factor_analyzer
#        OU installez une version compatible :
#        pip install factor_analyzer==0.5.1 scikit-learn==1.3.2

try:
    fa = FactorAnalyzer(n_factors=n_facteurs, rotation="varimax", method="principal")
    fa.fit(X_scaled)
    print(f"  ✓ {n_facteurs} facteurs extraits avec rotation Varimax")
    use_fa = True
except TypeError as e:
    print(f"  ⚠️ Erreur de compatibilité factor_analyzer/scikit-learn : {e}")
    print("  → Solution : pip install --upgrade factor_analyzer")
    print("  → Alternative : On utilise l'ACP avec rotation manuelle...")

    # Alternative : utiliser PCA + rotation varimax manuelle
    from scipy.linalg import svd

    # Extraire les loadings via PCA
    pca_fa = PCA(n_components=n_facteurs)
    pca_fa.fit(X_scaled)

    # Loadings = composantes * sqrt(valeurs propres)
    loadings_raw = pca_fa.components_.T * np.sqrt(pca_fa.explained_variance_)

    # Rotation Varimax simplifiée
    def varimax_rotation(loadings, max_iter=100, tol=1e-6):
        """Rotation Varimax simplifiée."""
        n_vars, n_factors = loadings.shape
        rotation_matrix = np.eye(n_factors)
        var_old = 0

        for _ in range(max_iter):
            rotated = loadings @ rotation_matrix

            # Critère varimax
            u, s, vh = svd(
                loadings.T
                @ (rotated**3 - rotated @ np.diag(np.sum(rotated**2, axis=0)) / n_vars)
            )
            rotation_matrix = u @ vh

            var_new = (
                np.sum(rotated**4) - np.sum(np.sum(rotated**2, axis=0) ** 2) / n_vars
            )
            if abs(var_new - var_old) < tol:
                break
            var_old = var_new

        return loadings @ rotation_matrix

    loadings_rotated = varimax_rotation(loadings_raw)

    # Créer un objet factice pour stocker les loadings
    class FakeFA:
        def __init__(self, loadings):
            self.loadings_ = loadings

    fa = FakeFA(loadings_rotated)
    use_fa = True
    print(f"  ✓ {n_facteurs} facteurs extraits (méthode alternative)")


# ==============================================================================
# 5.4 MATRICE DES LOADINGS
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QU'EST-CE QU'UN LOADING ?                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Le LOADING dit : "À quel point cette variable APPARTIENT à ce facteur"      ║
║                                                                              ║
║  C'est un nombre entre -1 et +1 :                                            ║
║  • Loading = 0.85 → "Cette variable DÉFINIT ce facteur" (très fort)          ║
║  • Loading = 0.50 → "Cette variable FAIT PARTIE du facteur" (moyen)          ║
║  • Loading = 0.20 → "Lien faible" (pas vraiment dans ce facteur)             ║
║                                                                              ║
║  📏 RÈGLE SIMPLE :                                                           ║
║     |Loading| ≥ 0.5 → Variable IMPORTANTE pour ce facteur ✓                  ║
║     |Loading| < 0.3 → Variable PAS dans ce facteur ✗                         ║
║                                                                              ║
║  EXEMPLE DE LECTURE :                                                        ║
║  ┌─────────────────────────┬──────────┬──────────┬──────────┐                ║
║  │ Variable                │ Facteur1 │ Facteur2 │ Facteur3 │                ║
║  ├─────────────────────────┼──────────┼──────────┼──────────┤                ║
║  │ qualite_nourriture      │   0.85   │   0.10   │   0.05   │                ║
║  │ rapidite_service        │   0.08   │   0.82   │   0.11   │                ║
║  │ proprete_restaurant     │   0.10   │   0.08   │   0.88   │                ║
║  └─────────────────────────┴──────────┴──────────┴──────────┘                ║
║                                                                              ║
║  LECTURE :                                                                   ║
║  • qualite_nourriture a loading 0.85 sur Facteur1, mais 0.10 sur Facteur2    ║
║    → Elle APPARTIENT clairement au Facteur 1                                 ║
║                                                                              ║
║  • rapidite_service a loading 0.82 sur Facteur2, mais 0.08 sur Facteur1      ║
║    → Elle APPARTIENT clairement au Facteur 2                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- 5.4 Matrice des loadings ---")
print("  (Rappel : |Loading| ≥ 0.5 = variable IMPORTANTE pour ce facteur)")

loadings_fa = pd.DataFrame(
    fa.loadings_,
    columns=[f"Facteur_{i + 1}" for i in range(n_facteurs)],
    index=X.columns,
)

print("\n" + loadings_fa.round(3).to_string())


# ==============================================================================
# 5.5 INTERPRÉTATION DES FACTEURS
# ==============================================================================

print("\n--- 5.5 Interprétation des facteurs ---")
print("  (Variables avec |loading| ≥ 0.4)")

for i in range(n_facteurs):
    facteur = f"Facteur_{i + 1}"
    fortes = loadings_fa[facteur][abs(loadings_fa[facteur]) >= 0.4].sort_values(
        key=abs, ascending=False
    )

    print(f"\n  {facteur} :")
    for var, val in fortes.items():
        signe = "+" if val > 0 else "-"
        barre = "█" * int(abs(val) * 10)
        print(f"    {signe} {var:30} {val:+.3f} {barre}")

# Proposer des noms
print("\n--- 5.6 Noms proposés pour les facteurs ---")

noms_facteurs = {
    "Facteur_1": "QUALITÉ_CUISINE",
    "Facteur_2": "QUALITÉ_SERVICE",
    "Facteur_3": "AMBIANCE_CONFORT",
}

for f, nom in noms_facteurs.items():
    print(f"  {f} → '{nom}'")

# Visualisation
print("\n--- 5.7 Visualisation ---")

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    loadings_fa, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, linewidths=0.5
)
ax.set_title(
    "Loadings après rotation Varimax\n(|valeur| ≥ 0.5 = lien fort)", fontweight="bold"
)
plt.tight_layout()
plt.savefig("etape5_af.png", dpi=150)
plt.close()

print("  ✓ Graphique sauvegardé : etape5_af.png")


# ==============================================================================
# BILAN FINAL
# ==============================================================================

print("\n" + "=" * 80)
print("BILAN FINAL : ÉTAPES 1 À 5")
print("=" * 80)
print(f"""
  ╔════════════════════════════════════════════════════════════════════════════╗
  ║                           RÉCAPITULATIF                                    ║
  ╠════════════════════════════════════════════════════════════════════════════╣
  ║                                                                            ║
  ║  ÉTAPE 1 : NETTOYAGE ✓                                                     ║
  ║            → Données propres (NA traités, pas d'erreur NaN possible)       ║
  ║                                                                            ║
  ║  ÉTAPE 2 : STANDARDISATION ✓                                               ║
  ║            → Variables comparables (moyenne=0, écart-type=1)               ║
  ║                                                                            ║
  ║  ÉTAPE 3 : CORRÉLATIONS ✓                                                  ║
  ║            → Structure en 3 groupes visible                                ║
  ║                                                                            ║
  ║  ÉTAPE 4 : ACP ✓                                                           ║
  ║            → {n_kaiser} dimensions principales (critère de Kaiser)              ║
  ║                                                                            ║
  ║  ÉTAPE 5 : ANALYSE FACTORIELLE ✓                                           ║
  ║            → {n_facteurs} facteurs nommés : Cuisine, Service, Ambiance           ║
  ║                                                                            ║
  ╠════════════════════════════════════════════════════════════════════════════╣
  ║                                                                            ║
  ║  🔗 LIEN CLÉ : ACP → Analyse Factorielle                                   ║
  ║  ─────────────────────────────────────────                                 ║
  ║  L'ACP dit COMBIEN de dimensions ? → {n_kaiser}                                 ║
  ║  L'AF dit QUELLES SONT ces dimensions ? → Cuisine, Service, Ambiance       ║
  ║                                                                            ║
  ║  Comment on sait quelles variables vont dans quel facteur ?                ║
  ║  → On regarde les LOADINGS ! Loading ≥ 0.5 = appartient au facteur         ║
  ║                                                                            ║
  ╚════════════════════════════════════════════════════════════════════════════╝
  
  📁 FICHIERS GÉNÉRÉS :
  • etape3_correlations.png
  • etape4_acp.png
  • etape5_af.png
""")


################################################################################
#                    ÉTAPE 6 : RÉGRESSION MULTIPLE                             #
################################################################################

print("\n" + "=" * 80)
print("ÉTAPE 6 : RÉGRESSION MULTIPLE")
print("=" * 80)

# ==============================================================================
# 6.1 CRÉATION DU MODÈLE DE RÉGRESSION
# ==============================================================================
"""
La régression multiple modélise Y en fonction de plusieurs X :

Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ + ε

- β₀ : l'intercept (valeur de Y quand tous les X = 0)
- βᵢ : coefficient de Xᵢ (impact de Xᵢ sur Y)
- ε : erreur (ce que le modèle n'explique pas)
"""

print("\n--- 6.1 Création du modèle ---")

# Ajouter une constante (intercept) aux variables X
X_reg = sm.add_constant(X)

# Créer et ajuster le modèle OLS (Ordinary Least Squares)
model = sm.OLS(y, X_reg).fit()
#       ↑                  ↑
#       |                  Ajuster le modèle aux données
#       Ordinary Least Squares (moindres carrés ordinaires)

print("  ✓ Modèle OLS créé et ajusté")

# ==============================================================================
# 6.2 RÉSUMÉ DU MODÈLE
# ==============================================================================

print("\n--- 6.2 Résumé du modèle ---")
print(model.summary())

# ==============================================================================
# 6.3 EXTRACTION DES COEFFICIENTS
# ==============================================================================

print("\n--- 6.3 Coefficients et significativité ---")

# Extraire les coefficients
coefs = model.params
pvalues = model.pvalues

print("\n" + "-" * 70)
print(f"{'Variable':<30} | {'Coefficient':>12} | {'p-value':>10} | Signif.")
print("-" * 70)

for var in coefs.index:
    coef = coefs[var]
    pval = pvalues[var]

    # Déterminer la significativité
    if pval < 0.001:
        signif = "***"
    elif pval < 0.01:
        signif = "**"
    elif pval < 0.05:
        signif = "*"
    else:
        signif = ""

    print(f"{var:<30} | {coef:>+12.4f} | {pval:>10.4f} | {signif}")

print("-" * 70)
print("  *** p < 0.001  |  ** p < 0.01  |  * p < 0.05")

# ==============================================================================
# 6.4 QUALITÉ DU MODÈLE
# ==============================================================================

print("\n--- 6.4 Qualité du modèle ---")

print(f"""
  R²          = {model.rsquared:.4f}  ({model.rsquared * 100:.1f}% de variance expliquée)
  R² ajusté   = {model.rsquared_adj:.4f}  (pénalise le nombre de variables)
  
  Interprétation :
  → R² = {model.rsquared:.1%} signifie que le modèle explique {model.rsquared * 100:.1f}%
    de la variabilité de la satisfaction.
  → Les {(1 - model.rsquared) * 100:.1f}% restants sont dus à d'autres facteurs non mesurés.
""")

################################################################################
#                                                                              #
#                 DIAGNOSTICS DE LA RÉGRESSION (ÉTAPE 6)                       #
#                                                                              #
################################################################################
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              POURQUOI VÉRIFIER LES DIAGNOSTICS ?                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  La régression linéaire repose sur des HYPOTHÈSES.                           ║
║  Si ces hypothèses ne sont pas respectées :                                  ║
║  - Les coefficients peuvent être BIAISÉS                                     ║
║  - Les p-values et intervalles de confiance sont FAUX                        ║
║  - Le modèle fait de mauvaises prédictions                                   ║
║                                                                              ║
║  Les 3 hypothèses principales à vérifier :                                   ║
║                                                                              ║
║  1. NORMALITÉ DES RÉSIDUS                                                    ║
║     Les erreurs du modèle doivent suivre une loi normale.                    ║
║     Test : Shapiro-Wilk                                                      ║
║                                                                              ║
║  2. HOMOSCÉDASTICITÉ                                                         ║
║     La variance des erreurs doit être CONSTANTE.                             ║
║     Test : Breusch-Pagan                                                     ║
║                                                                              ║
║  3. ABSENCE DE MULTICOLINÉARITÉ                                              ║
║     Les variables X ne doivent pas être trop corrélées entre elles.          ║
║     Mesure : VIF (Variance Inflation Factor)                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n" + "=" * 80)
print("DIAGNOSTICS DU MODÈLE DE RÉGRESSION")
print("=" * 80)

# ==============================================================================
# DIAGNOSTIC 1 : NORMALITÉ DES RÉSIDUS (Test de Shapiro-Wilk)
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       QU'EST-CE QU'UN RÉSIDU ?                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Résidu = Valeur observée - Valeur prédite                                   ║
║                                                                              ║
║  Résidu = Y - Ŷ                                                              ║
║           ↑   ↑                                                              ║
║           |   Valeur prédite par le modèle                                   ║
║           Valeur réelle                                                      ║
║                                                                              ║
║  Les résidus représentent ce que le modèle n'a PAS réussi à expliquer.       ║
║  C'est l'"erreur" du modèle.                                                 ║
║                                                                              ║
║  EXEMPLE :                                                                   ║
║  - Un client a une satisfaction réelle de 8                                  ║
║  - Le modèle prédit 7.2                                                      ║
║  - Résidu = 8 - 7.2 = 0.8 (le modèle a sous-estimé de 0.8)                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEST DE SHAPIRO-WILK                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Ce test vérifie si les données suivent une distribution NORMALE.            ║
║                                                                              ║
║  HYPOTHÈSES :                                                                ║
║  - H0 : Les données suivent une loi normale                                  ║
║  - H1 : Les données ne suivent PAS une loi normale                           ║
║                                                                              ║
║  INTERPRÉTATION :                                                            ║
║  - p > 0.05 : On NE REJETTE PAS H0 → Résidus normaux ✓                       ║
║  - p < 0.05 : On REJETTE H0 → Résidus NON normaux ⚠️                         ║
║                                                                              ║
║  ATTENTION : Le test est sensible à la taille d'échantillon.                 ║
║  Avec N > 5000, il détecte souvent des écarts mineurs non problématiques.    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- Diagnostic 1 : NORMALITÉ DES RÉSIDUS ---")

# Récupérer les résidus du modèle
"""
model.resid :
    Attribut qui contient les résidus (erreurs) du modèle.
    C'est un pandas Series avec un résidu pour chaque observation.
"""

residus = model.resid
#               ↑
#               Attribut du modèle statsmodels

print(f"\nNombre de résidus : {len(residus)}")
print(f"Moyenne des résidus : {residus.mean():.6f}")
print("  (devrait être proche de 0)")

# Test de Shapiro-Wilk
"""
shapiro(données) de scipy.stats :

Retourne :
- stat : la statistique W du test (proche de 1 = normal)
- p_value : la probabilité d'observer ce résultat si les données étaient normales
"""

stat_shapiro, p_shapiro = shapiro(residus)
#                         ↑
#                         Fonction de scipy.stats
#                         Retourne 2 valeurs

print("\nTest de Shapiro-Wilk :")
print(f"  Statistique W : {stat_shapiro:.4f}")
print("    (W proche de 1 = données proches de la normale)")
print(f"  p-value : {p_shapiro:.4f}")

# Interprétation
"""
On compare la p-value au seuil de 0.05 (5%).

Si p > 0.05 : pas assez de preuves pour rejeter H0
→ On suppose que les résidus sont normaux

Si p < 0.05 : on rejette H0
→ Les résidus ne sont pas normaux
"""

if p_shapiro > 0.05:
    print("\n  ✓ p > 0.05 → On ne rejette pas H0")
    print("  → Les résidus suivent une distribution NORMALE")
    normalite_ok = True
else:
    print("\n  ⚠️ p < 0.05 → On rejette H0")
    print("  → Les résidus ne suivent PAS une distribution normale")
    print("  → Solutions : transformer Y (log), utiliser régression robuste")
    normalite_ok = False

# ==============================================================================
# DIAGNOSTIC 2 : HOMOSCÉDASTICITÉ (Test de Breusch-Pagan)
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QU'EST-CE QUE L'HOMOSCÉDASTICITÉ ?                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HOMOSCÉDASTICITÉ = Variance CONSTANTE des résidus                           ║
║  (du grec "homos" = même, "skedasis" = dispersion)                           ║
║                                                                              ║
║  Cela signifie que la "dispersion" des erreurs est la même                   ║
║  pour toutes les valeurs prédites.                                           ║
║                                                                              ║
║  HÉTÉROSCÉDASTICITÉ = Variance NON constante (problème !)                    ║
║  La dispersion des erreurs change selon les valeurs prédites.                ║
║                                                                              ║
║  VISUALISATION :                                                             ║
║                                                                              ║
║  HOMOSCÉDASTICITÉ (OK) :        HÉTÉROSCÉDASTICITÉ (Problème) :              ║
║                                                                              ║
║  Résidus                        Résidus                                      ║
║     ↑    · · · · ·                 ↑         ·  ·                            ║
║     │  · · · · · · ·               │       ·  ·  ·                           ║
║   0 │──·─·─·─·─·─·─·──            0 │──·─·─────────                          ║
║     │  · · · · · · ·               │     ·  ·  ·                             ║
║     │    · · · · ·                 │  ·   ·  ·                               ║
║     └───────────────→              └───────────────→                         ║
║          Valeurs prédites               Valeurs prédites                     ║
║                                                                              ║
║  Les points forment un "tube"    Les points forment un "cône"                ║
║  de largeur constante.           qui s'élargit.                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEST DE BREUSCH-PAGAN                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Ce test vérifie si la variance des résidus est constante.                   ║
║                                                                              ║
║  HYPOTHÈSES :                                                                ║
║  - H0 : Homoscédasticité (variance constante) ✓                              ║
║  - H1 : Hétéroscédasticité (variance non constante) ⚠️                       ║
║                                                                              ║
║  INTERPRÉTATION :                                                            ║
║  - p > 0.05 : On ne rejette pas H0 → Homoscédasticité ✓                      ║
║  - p < 0.05 : On rejette H0 → Hétéroscédasticité ⚠️                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- Diagnostic 2 : HOMOSCÉDASTICITÉ ---")

# Test de Breusch-Pagan
"""
het_breuschpagan(residus, exog) de statsmodels :

PARAMÈTRES :
- residus : les résidus du modèle
- exog : les variables explicatives (avec constante)
  model.model.exog contient les X utilisés dans la régression

RETOURNE 4 valeurs :
- lm_stat : statistique LM du test
- lm_pvalue : p-value pour la statistique LM
- f_stat : statistique F du test
- f_pvalue : p-value pour la statistique F

On utilise généralement lm_pvalue.
"""

bp_lm, bp_pvalue, bp_f, bp_f_pvalue = het_breuschpagan(residus, model.model.exog)
#                                     ↑                 ↑            ↑
#                                     |                 |            Variables X du modèle
#                                     |                 Les résidus
#                                     Fonction de statsmodels

print("\nTest de Breusch-Pagan :")
print(f"  Statistique LM : {bp_lm:.4f}")
print(f"  p-value : {bp_pvalue:.4f}")

# Interprétation
if bp_pvalue > 0.05:
    print("\n  ✓ p > 0.05 → On ne rejette pas H0")
    print("  → HOMOSCÉDASTICITÉ : la variance des résidus est CONSTANTE")
    homoscedasticite_ok = True
else:
    print("\n  ⚠️ p < 0.05 → On rejette H0")
    print("  → HÉTÉROSCÉDASTICITÉ : la variance des résidus n'est pas constante")
    print("  → Solutions : erreurs robustes (HC3), transformation de Y")
    homoscedasticite_ok = False

# ==============================================================================
# DIAGNOSTIC 3 : MULTICOLINÉARITÉ (VIF - Variance Inflation Factor)
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QU'EST-CE QUE LA MULTICOLINÉARITÉ ?                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  La multicolinéarité survient quand des variables X sont                     ║
║  FORTEMENT CORRÉLÉES entre elles.                                            ║
║                                                                              ║
║  EXEMPLE :                                                                   ║
║  - X1 = taille en cm                                                         ║
║  - X2 = taille en pouces                                                     ║
║  → X1 et X2 sont parfaitement corrélées (multicolinéarité parfaite)          ║
║                                                                              ║
║  POURQUOI C'EST UN PROBLÈME ?                                                ║
║  - Les coefficients deviennent INSTABLES                                     ║
║  - Difficile d'isoler l'effet de chaque variable                             ║
║  - Les erreurs standard sont GONFLÉES (d'où le nom VIF)                      ║
║  - Les p-values sont faussées                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                    QU'EST-CE QUE LE VIF ?                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  VIF = Variance Inflation Factor (Facteur d'Inflation de la Variance)        ║
║                                                                              ║
║  FORMULE :                                                                   ║
║                    1                                                         ║
║  VIF_i = ─────────────────                                                   ║
║           1 - R²_i                                                           ║
║                                                                              ║
║  Où R²_i est le R² obtenu en régressant X_i sur toutes les autres X.         ║
║                                                                              ║
║  INTERPRÉTATION :                                                            ║
║  - VIF = 1 : pas de multicolinéarité (X_i n'est pas corrélé aux autres)      ║
║  - VIF > 1 : il y a de la multicolinéarité                                   ║
║                                                                              ║
║  SEUILS CLASSIQUES :                                                         ║
║  - VIF < 5 : Acceptable ✓                                                    ║
║  - 5 ≤ VIF < 10 : Problématique ⚠️                                           ║
║  - VIF ≥ 10 : Sévère ✗ (à traiter absolument)                                ║
║                                                                              ║
║  EXEMPLE D'INTERPRÉTATION :                                                  ║
║  VIF = 4 signifie que la variance du coefficient est 4× plus grande          ║
║  qu'elle ne le serait sans multicolinéarité.                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

print("\n--- Diagnostic 3 : MULTICOLINÉARITÉ (VIF) ---")

# Ajouter une constante aux données X
"""
sm.add_constant(X) :
    Ajoute une colonne de 1 au début du DataFrame.
    C'est nécessaire car variance_inflation_factor attend une constante.
    
    Avant : [X1, X2, X3]
    Après : [const, X1, X2, X3] où const = [1, 1, 1, ...]
"""

X_avec_const = sm.add_constant(X)
#              ↑
#              Ajoute une colonne 'const' avec des 1

print("\nVIF par variable :")
print("-" * 60)
print(f"{'Variable':<35} | {'VIF':>10} | {'Statut'}")
print("-" * 60)

# Variable pour suivre si tout est OK
vif_ok = True

# Calculer le VIF pour chaque variable
"""
enumerate(X.columns) :
    Donne l'index (i) et le nom de la variable (col) à chaque itération.
    i commence à 0.

variance_inflation_factor(X_avec_const.values, i+1) :
    - X_avec_const.values : convertit le DataFrame en array numpy
    - i+1 : index de la colonne (i+1 car la colonne 0 est la constante)
    
    La fonction calcule le VIF pour la colonne à l'index donné.
"""

for i, col in enumerate(X.columns):
    #   ↑  ↑
    #   |  Nom de la variable
    #   Index (0, 1, 2, ...)

    # Calculer le VIF
    # i+1 car l'index 0 est la constante
    vif = variance_inflation_factor(X_avec_const.values, i + 1)
    #                               ↑                    ↑
    #                               |                    Index de la colonne
    #                               Les données en format numpy

    # Déterminer le statut
    if vif < 5:
        status = "✓ OK"
    elif vif < 10:
        status = "⚠️ Modéré"
        vif_ok = False
    else:
        status = "✗ Sévère"
        vif_ok = False

    # Afficher
    print(f"{col:<35} | {vif:>10.2f} | {status}")

print("-" * 60)

# Interprétation globale
if vif_ok:
    print("\n✓ Tous les VIF < 5 → Pas de multicolinéarité problématique")
else:
    print("\n⚠️ Certains VIF ≥ 5 → Multicolinéarité détectée")
    print("   Solutions :")
    print("   - Retirer une des variables corrélées")
    print("   - Combiner les variables (moyenne, ACP)")
    print("   - Utiliser une régression Ridge")

# ==============================================================================
# RÉSUMÉ DES DIAGNOSTICS
# ==============================================================================

print("\n" + "=" * 80)
print("RÉSUMÉ DES DIAGNOSTICS")
print("=" * 80)

print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ Diagnostic              │ Test            │ Résultat    │ Statut           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Normalité résidus    │ Shapiro-Wilk    │ p = {p_shapiro:.4f} │ {"✓ OK" if normalite_ok else "⚠️ Problème":^16} │
│ 2. Homoscédasticité     │ Breusch-Pagan   │ p = {bp_pvalue:.4f} │ {"✓ OK" if homoscedasticite_ok else "⚠️ Problème":^16} │
│ 3. Multicolinéarité     │ VIF < 5         │ {"Tous < 5" if vif_ok else "Certains ≥ 5":^11} │ {"✓ OK" if vif_ok else "⚠️ Problème":^16} │
└─────────────────────────────────────────────────────────────────────────────┘
""")

if normalite_ok and homoscedasticite_ok and vif_ok:
    print("→ TOUS LES DIAGNOSTICS SONT SATISFAITS ✓")
    print("  Le modèle est valide pour l'inférence statistique.")
    print("  Les coefficients et p-values sont fiables.")
else:
    print("→ ATTENTION : Certains diagnostics ne sont pas satisfaits ⚠️")
    print("  Les résultats doivent être interprétés avec prudence.")
    print("  Envisagez les solutions proposées ci-dessus.")


# ==============================================================================
# 6.5 VISUALISATION DES DIAGNOSTICS
# ==============================================================================

print("\n--- 6.5 Visualisation ---")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Résidus vs Prédictions
ax1 = axes[0, 0]
ax1.scatter(model.fittedvalues, residus, alpha=0.5)
ax1.axhline(y=0, color="red", linestyle="--")
ax1.set_xlabel("Valeurs prédites")
ax1.set_ylabel("Résidus")
ax1.set_title("Résidus vs Prédictions (Homoscédasticité)")

# QQ-Plot
ax2 = axes[0, 1]
stats.probplot(residus, dist="norm", plot=ax2)
ax2.set_title("QQ-Plot (Normalité)")

# Histogramme des résidus
ax3 = axes[1, 0]
ax3.hist(residus, bins=30, edgecolor="white", density=True)
x = np.linspace(residus.min(), residus.max(), 100)
ax3.plot(x, stats.norm.pdf(x, 0, residus.std()), "r-", linewidth=2)
ax3.set_title("Distribution des résidus")

# Coefficients - CORRECTION ICI : 'const' au lieu de 'Intercept'
ax4 = axes[1, 1]
coefs_plot = coefs.drop("const").sort_values()  # ← CHANGÉ ICI
colors = ["green" if pvalues[c] < 0.05 else "gray" for c in coefs_plot.index]
coefs_plot.plot(kind="barh", ax=ax4, color=colors)
ax4.axvline(x=0, color="red", linestyle="--")
ax4.set_title("Coefficients (vert = significatif)")

plt.tight_layout()
plt.savefig("etape6_regression.png", dpi=150)
plt.close()
print("✓ Graphique sauvegardé : etape6_regression.png")


################################################################################
#                                                                              #
#                ÉTAPE 7 : INTERPRÉTATION ET RECOMMANDATIONS                   #
#                                                                              #
################################################################################

print("\n" + "=" * 80)
print("ÉTAPE 7 : INTERPRÉTATION MÉTIER ET RECOMMANDATIONS")
print("=" * 80)

# ==============================================================================
# 7.1 RÉSUMÉ EXÉCUTIF
# ==============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           RAPPORT D'ANALYSE                                  ║
║                     Satisfaction Client - Restaurant                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

CONTEXTE :
----------
Analyse de la satisfaction de 500 clients basée sur 10 critères d'évaluation.

OBJECTIF :
----------
Identifier les leviers d'action pour améliorer la satisfaction globale.
""")

# ==============================================================================
# 7.2 RÉSULTATS CLÉS
# ==============================================================================

print("\n" + "=" * 60)
print("RÉSULTATS CLÉS")
print("=" * 60)

# Top 3 des variables les plus influentes - CORRECTION ICI
coefs_significatifs = coefs.drop("const")  # ← CHANGÉ ICI
coefs_significatifs = coefs_significatifs[pvalues.drop("const") < 0.05]  # ← CHANGÉ ICI
top3 = coefs_significatifs.abs().sort_values(ascending=False).head(3)

print("\n1. TOP 3 DES FACTEURS D'INFLUENCE :")
print("-" * 50)
for i, (var, val) in enumerate(top3.items(), 1):
    coef = coefs[var]
    print(f"   {i}. {var}")
    print(f"      → +1 point sur cette note = {coef:+.3f} pts de satisfaction")
    print()

print("\n2. QUALITÉ DU MODÈLE :")
print("-" * 50)
print(f"   R² = {model.rsquared:.1%} de la satisfaction expliquée")
print(
    f"   → {'Excellent' if model.rsquared >= 0.7 else 'Bon' if model.rsquared >= 0.5 else 'Modéré'}"
)

print("\n3. STRUCTURE DE LA SATISFACTION :")
print("-" * 50)
print("   3 dimensions identifiées par l'analyse factorielle :")
print("   • CUISINE (qualité, présentation, fraîcheur)")
print("   • SERVICE (rapidité, amabilité, compétence)")
print("   • AMBIANCE (propreté, ambiance, confort)")

# ==============================================================================
# 7.3 RECOMMANDATIONS
# ==============================================================================

print("\n" + "=" * 60)
print("RECOMMANDATIONS OPÉRATIONNELLES")
print("=" * 60)

print("""
PRIORITÉ HAUTE 🔴 :
-------------------
• Améliorer la QUALITÉ DE LA NOURRITURE
  → Impact le plus fort sur la satisfaction
  → Actions : contrôle qualité, formation chefs, ingrédients premium

PRIORITÉ MOYENNE 🟡 :
--------------------
• Améliorer la RAPIDITÉ DU SERVICE
  → Second facteur d'importance
  → Actions : optimisation des process, effectifs aux heures de pointe

PRIORITÉ NORMALE 🟢 :
--------------------
• Maintenir la PROPRETÉ et l'AMBIANCE
  → Contributeurs modérés mais attendus comme baseline
  → Actions : checklists nettoyage, maintenance régulière
""")

# ==============================================================================
# 7.4 EXEMPLE DE PRÉDICTION
# ==============================================================================

print("\n" + "=" * 60)
print("EXEMPLE D'UTILISATION DU MODÈLE")
print("=" * 60)

client_test = pd.DataFrame(
    {
        "qualite_nourriture": [8],
        "presentation_plats": [7],
        "fraicheur_ingredients": [8],
        "rapidite_service": [6],
        "amabilite_personnel": [7],
        "competence_serveur": [7],
        "proprete_restaurant": [8],
        "ambiance": [7],
        "confort_siege": [6],
        "rapport_qualite_prix": [7],
    }
)

# CORRECTION : Ajouter la constante avant la prédiction
client_test_avec_const = sm.add_constant(client_test, has_constant="add")

prediction = model.predict(client_test_avec_const)[0]

print("\nProfil client :")
for col, val in client_test.iloc[0].items():
    print(f"  • {col:30} : {val}/10")

print(f"\n→ SATISFACTION PRÉDITE : {prediction:.1f}/10")
print(
    f"  Interprétation : Client {'satisfait' if prediction >= 7 else 'moyennement satisfait'}"
)

# ==============================================================================
# 7.5 LIMITES
# ==============================================================================

print("\n" + "=" * 60)
print("LIMITES DE L'ANALYSE")
print("=" * 60)
print("""
1. CORRÉLATION ≠ CAUSALITÉ
   Les corrélations observées ne prouvent pas de lien de cause à effet.

2. DONNÉES SIMULÉES
   Ce tutoriel utilise des données simulées pour l'apprentissage.
   Avec de vraies données, les résultats pourraient être différents.

3. VARIABLES OMISES
   D'autres facteurs non mesurés peuvent influencer la satisfaction
   (prix, localisation, météo, humeur du client...).

4. LINÉARITÉ
   Le modèle suppose des relations linéaires, ce qui est une simplification.
""")

# ==============================================================================
# FIN DU PROJET
# ==============================================================================

print("\n" + "=" * 80)
print("FIN DU PROJET - RÉCAPITULATIF")
print("=" * 80)
print(f"""
ÉTAPES COMPLÉTÉES :
-------------------
✓ Étape 1 : Nettoyage des données ({na_total} NA traités)
✓ Étape 2 : Standardisation (Z-score)
✓ Étape 3 : Analyse des corrélations ({len(correlations_fortes)} paires fortes)
✓ Étape 4 : ACP ({n_composantes} composantes, {variance_cumulee[n_composantes - 1] * 100:.1f}% variance)
✓ Étape 5 : Analyse Factorielle (KMO={kmo_total:.3f}, 3 facteurs)
✓ Étape 6 : Régression Multiple (R²={model.rsquared:.3f})
✓ Étape 7 : Interprétation et recommandations

FICHIERS GÉNÉRÉS :
------------------
• etape1_distributions.png
• etape3_correlations.png
• etape6_regression.png

Ce projet peut servir de TEMPLATE pour vos propres analyses.
Remplacez les données simulées par vos vraies données !

Formation Utopios - Mohamed 2026
""")
