import pandas as pd

# Transformateur de données

class DataTransformer:
    """Transformateur de données"""

    def __init__(self, logger):
        self.logger = logger

    def clean(self, df):
        """Nettoie les données"""
        try:
            self.logger.info("Nettoyage des données")
            initial_count = len(df)

            # Supprimer doublons (lignes identiques)
            df = df.drop_duplicates()
            self.logger.info(f"  - {initial_count - len(df)} doublons supprimés")

            # Supprimer colonnes vides (toutes les valeurs NaN)
            df = df.dropna(axis=1, how='all')

            # Trim des espaces dans les colonnes de type string (object)
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip()

            self.logger.info(f"Nettoyage terminé: {len(df)} lignes")
            return df

        except Exception as e:
            self.logger.error(f"Erreur nettoyage: {e}")
            raise

    def validate(self, df, required_columns):
        """Valide la structure des données"""
        # On vérifie que toutes les colonnes requises sont présentes
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            # On lève une erreur explicite si des colonnes manquent
            raise ValueError(f"Colonnes manquantes: {missing_cols}")

        self.logger.info("Validation réussie")
        return True

    def enrich(self, df, enrichment_func):
        """Enrichit les données"""
        try:
            self.logger.info("Enrichissement des données")
            # On délègue la logique d'enrichissement à une fonction externe
            df = enrichment_func(df)
            self.logger.info("Enrichissement terminé")
            return df
        except Exception as e:
            self.logger.error(f"Erreur enrichissement: {e}")
            raise