# TP 2 - Web Scraping

Ce TP a pour objectif de scraper plusieurs pages du site "http://quotes.toscrape.com".

## Structure du Projet

```
├───config
├───logs
├───output
└───src
```

## Librairies Utilisées

- **requests**
- **urllib**
- **beautifulsoup4**
- **lxml**
- **pandas**

## Installation & Lancement

Récupérer le TP en clonant le ripository GitHub :

```bash
git clone https://github.com/DamienDESSAUX-M2i/M2i_CDSD_TDTP.git
```

Installer les bilbliothèques :

```bash
pip install requests urllib beautifulsoup4 lxml pandas
```

Placez vous dans le dossier `M2i_CDSD_TDTP/web_scraping/exos/tp2/`, puis lancer le TP avec la commande :

```bash
python main.py
```

Un rapport excel sera généré dans le dossier `output/`.

Le rapport contient :
- une feuille avec les citations et leur longueur
- une feuille avec les auteurs et leur nombre de citations
- une feuille avec les tags et leur nombre d'occurrences
- le top 5 des auteurs les plus cités
- le top 10 des tags les plus utilisés
- la longueur moyenne des citations

Vous pouvez changer le nombre maximum de pages scapper dans le fichier `config/config.yaml`.

