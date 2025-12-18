"""Client MinIO pour le stockage d'objets."""

import io
import json
from datetime import datetime
from typing import Optional

import structlog
from config.settings import minio_config
from minio.error import S3Error

from minio import Minio

logger = structlog.get_logger()


class MinIOStorage:
    def __init__(self):
        self.client = Minio(
            endpoint=minio_config.endpoint,
            access_key=minio_config.access_key,
            secret_key=minio_config.secret_key,
            secure=minio_config.secure,
        )
        self._ensure_buckets()

    def _ensure_buckets(self) -> None:
        buckets = [
            minio_config.bucket_backups,
            minio_config.bucket_exports,
            minio_config.bucket_images,
        ]

        for bucket in buckets:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

    def upload_export(
        self, data: bytes, filename: str, content_type: str = "application/octet-stream"
    ) -> Optional[str]:
        """
        Upload un fichier d'export.

        Args:
            data: Contenu du fichier
            filename: Nom du fichier
            content_type: Type MIME

        Returns:
            URI MinIO ou None
        """
        try:
            self.client.put_object(
                bucket_name=minio_config.bucket_exports,
                object_name=filename,
                data=io.BytesIO(data),
                length=len(data),
                content_type=content_type,
            )

            uri = f"minio://{minio_config.bucket_exports}/{filename}"
            logger.info("export_uploaded", filename=filename, size_kb=len(data) // 1024)
            return uri

        except S3Error as e:
            logger.error("upload_failed", filename=filename, error=str(e))
            return None

    def upload_json(self, data: dict, filename: str) -> Optional[str]:
        """Upload un fichier JSON."""
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        return self.upload_export(json_bytes, filename, "application/json")

    def upload_csv(self, csv_content: str, filename: str) -> Optional[str]:
        """Upload un fichier CSV."""
        return self.upload_export(csv_content.encode("utf-8"), filename, "text/csv")

    def create_backup(self, data: dict, prefix: str = "backup") -> Optional[str]:
        """
        Crée une sauvegarde horodatée.

        Args:
            data: Données à sauvegarder
            prefix: Préfixe du fichier

        Returns:
            URI MinIO
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.json"

        try:
            json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

            self.client.put_object(
                bucket_name=minio_config.bucket_backups,
                object_name=filename,
                data=io.BytesIO(json_bytes),
                length=len(json_bytes),
                content_type="application/json",
            )

            uri = f"minio://{minio_config.bucket_backups}/{filename}"
            logger.info("backup_created", filename=filename)
            return uri

        except S3Error as e:
            logger.error("backup_failed", error=str(e))
            return None

    def upload_image(
        self, image_data: bytes, filename: str, content_type: str = "image/jpeg"
    ) -> Optional[str]:
        """Upload une image d'auteur."""
        try:
            self.client.put_object(
                bucket_name=minio_config.bucket_images,
                object_name=filename,
                data=io.BytesIO(image_data),
                length=len(image_data),
                content_type=content_type,
            )

            return f"minio://{minio_config.bucket_images}/{filename}"

        except S3Error as e:
            logger.error("image_upload_failed", error=str(e))
            return None

    def get_object(self, bucket: str, filename: str) -> Optional[bytes]:
        """Télécharge un objet."""
        try:
            response = self.client.get_object(bucket, filename)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error:
            return None

    def list_objects(self, bucket: str, prefix: str = "") -> list[dict]:
        """Liste les objets d'un bucket."""
        objects = self.client.list_objects(bucket, prefix=prefix, recursive=True)
        return [
            {"name": obj.object_name, "size": obj.size, "modified": obj.last_modified}
            for obj in objects
        ]

    def list_exports(self) -> list[dict]:
        """Liste tous les exports."""
        return self.list_objects(minio_config.bucket_exports)

    def list_backups(self) -> list[dict]:
        """Liste toutes les sauvegardes."""
        return self.list_objects(minio_config.bucket_backups)

    def delete_object(self, bucket: str, filename: str) -> bool:
        """Supprime un objet."""
        try:
            self.client.remove_object(bucket, filename)
            return True
        except S3Error:
            return False

    def get_presigned_url(
        self, bucket: str, filename: str, expires_hours: int = 24
    ) -> Optional[str]:
        """Génère une URL temporaire."""
        from datetime import timedelta

        try:
            return self.client.presigned_get_object(
                bucket_name=bucket,
                object_name=filename,
                expires=timedelta(hours=expires_hours),
            )
        except S3Error:
            return None

    def get_storage_stats(self) -> dict:
        """Retourne les statistiques de stockage."""
        stats = {}

        for bucket in [minio_config.bucket_exports, minio_config.bucket_backups]:
            objects = self.list_objects(bucket)
            stats[bucket] = {
                "count": len(objects),
                "total_size_mb": sum(o["size"] for o in objects) / (1024 * 1024),
            }

        return stats
