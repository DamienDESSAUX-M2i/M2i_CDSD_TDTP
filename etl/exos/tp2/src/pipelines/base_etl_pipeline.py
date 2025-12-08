from abc import ABC, abstractmethod


class BaseETLPipeline(ABC):
    """Pipeline ETL complet"""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self):
        """Exécute le pipeline"""
        try:
            self.logger.info("=" * 3)
            self.logger.info("DÉBUT DU PIPELINE ETL")
            self.logger.info("=" * 3)

            # Extract
            self.logger.info("[1/3] EXTRACTION")
            data = self._extract()

            # Transform
            self.logger.info("[2/3] TRANSFORMATION")
            data_transformed = self._transform(data)

            # Load
            self.logger.info("[3/3] CHARGEMENT")
            self._load(data_transformed)

            self.logger.info("=" * 3)
            self.logger.info("PIPELINE TERMINÉ AVEC SUCCÈS")
            self.logger.info("=" * 3)

        except Exception as e:
            self.logger.error(f"\nPIPELINE ÉCHOUÉ: {e}")
            raise

    @abstractmethod
    def _extract(self):
        """Logique d'extraction"""
        raise NotImplementedError

    @abstractmethod
    def _transform(self, data):
        """Logique de transformation"""
        raise NotImplementedError

    @abstractmethod
    def _load(self, data):
        """Logique de chargement"""
        raise NotImplementedError
