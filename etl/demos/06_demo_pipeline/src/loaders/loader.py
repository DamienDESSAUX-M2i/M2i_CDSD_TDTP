import pandas as pd
from datetime import datetime

# Chargeur de données (vers CSV / Excel)


class DataLoader:
    """Chargeur de données"""

    def __init__(self, logger):
        self.logger = logger

    def load_csv(self, df, filepath, **kwargs):
        """Charge vers CSV"""
        try:
            self.logger.info(f"Chargement vers {filepath}")
            # Écriture du DataFrame dans un fichier CSV
            df.to_csv(filepath, index=False, **kwargs)
            self.logger.info(f"{len(df)} lignes chargées")
        except Exception as e:
            self.logger.error(f"Erreur chargement CSV: {e}")
            raise

    def load_excel(self, df, filepath, sheet_name='Data', **kwargs):
        """Charge vers Excel"""
        try:
            self.logger.info(f"Chargement vers {filepath}")

            # Utilisation de ExcelWriter pour gérer le fichier Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)

            self.logger.info(f"{len(df)} lignes chargées")
        except Exception as e:
            self.logger.error(f"Erreur chargement Excel: {e}")
            raise

    def load_multiple_sheets(self, dataframes_dict, filepath):
        """Charge plusieurs feuilles Excel"""
        try:
            self.logger.info(f"Chargement multi-feuilles vers {filepath}")

            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in dataframes_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    self.logger.info(f"  - Feuille '{sheet_name}': {len(df)} lignes")

            self.logger.info("Chargement terminé")
        except Exception as e:
            self.logger.error(f"Erreur chargement multi-feuilles: {e}")
            raise