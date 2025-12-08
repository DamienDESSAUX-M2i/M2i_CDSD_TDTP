from src.transformers.cleaner import DataTransformer
from src.loaders.loader import DataLoader

class ETLPipeline:
    """Pipeline ETL complet"""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.extractor = None
        self.transformer = DataTransformer(logger)
        self.loader = DataLoader(logger)

    def run(self):
        """Exécute le pipeline"""
        try:
            self.logger.info("="*50)
            self.logger.info("DÉBUT DU PIPELINE ETL")
            self.logger.info("="*50)

            # Extract
            self.logger.info("\n[1/3] EXTRACTION")
            data = self._extract()

            # Transform
            self.logger.info("\n[2/3] TRANSFORMATION")
            data_transformed = self._transform(data)

            # Load
            self.logger.info("\n[3/3] CHARGEMENT")
            self._load(data_transformed)

            self.logger.info("\n" + "="*50)
            self.logger.info("PIPELINE TERMINÉ AVEC SUCCÈS")
            self.logger.info("="*50)

        except Exception as e:
            self.logger.error(f"\nPIPELINE ÉCHOUÉ: {e}")
            raise

    def _extract(self):
        """Logique d'extraction"""
        pass

    def _transform(self, data):
        """Logique de transformation"""
        pass

    def _load(self, data):
        """Logique de chargement"""
        pass