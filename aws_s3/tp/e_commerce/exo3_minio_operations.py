import io
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from config import minio_config
from PIL import Image
from src.storage import MinIOStorage, MongoDBStorage

DIR_PATH = Path(__file__).parent.resolve()


def create_thumbnails(minio: MinIOStorage, list_filenames: dict) -> int:
    """Crée un thumbnail pour chaque image de produit"""
    thumbnails_created = 0
    for filename in list_filenames:
        image_byte = minio.get_object(
            bucket=minio_config.bucket_images, filename=filename
        )

        # Load byte object
        pil_image = Image.open(io.BytesIO(image_byte))
        pil_image.thumbnail((100, 100))

        # Pillow Image object to byte
        thumbnail_byte = io.BytesIO()
        pil_image.save(thumbnail_byte, format="PNG")
        thumbnail_byte = thumbnail_byte.getvalue()

        # Upload thumbnail image
        thumbnail_filename = "thumbnail/" + filename
        minio.upload_image(image_data=thumbnail_byte, filename=thumbnail_filename)

        thumbnails_created += 1
    return thumbnails_created


def exercise_3():
    minio = MinIOStorage()
    mongo = MongoDBStorage()

    # 3.1 Listez toutes les images et calculez la taille totale
    list_objects = minio.list_objects(bucket=minio_config.bucket_images)
    total_images = len(list_objects)
    total_size_kb = sum([object_info["size"] for object_info in list_objects])

    # 3.2 Créez des thumbnails (100x100) pour toutes les images
    # Stockez-les dans le même bucket avec préfixe "thumbnails/"
    # Indice: Utilisez PIL (Pillow)
    thumbnails_created = 0
    # list_filenames = [object_info["name"] for object_info in list_objects]
    # thumbnails_created = create_thumbnails(minio=minio, list_filenames=list_filenames)

    # 3.3 Générez une URL présignée (24h) pour l'image du produit le plus cher
    pipeline = [{"$sort": {"price": -1}}, {"$limit": 1}]
    product_most_expensive = list(mongo.products.aggregate(pipeline))[0]
    filename_product_most_expensive = "/".join(
        [
            product_most_expensive["category"],
            product_most_expensive["sub_category"],
            product_most_expensive["id_product"],
            ".jpeg",
        ]
    )
    presigned_url = minio.get_presigned_url(
        bucket=minio_config.bucket_images,
        filename=filename_product_most_expensive,
        expires_hours=24,
    )

    # 3.4 Créez un rapport JSON avec les stats de chaque catégorie d'images
    # et uploadez-le dans le bucket exports
    # Format: {"laptops": {"count": X, "size_kb": Y}, ...}
    objects_infos = deepcopy(list_objects)

    # Ajout d'information à partir du filename: thumbnail image, category et sub_category
    sub_categories = []
    for k in range(len(objects_infos)):
        filename = objects_infos[k]["name"]
        filename_split = filename.split("/")
        if "thumbnail" in filename_split:
            objects_infos[k]["thumbnail"] = True
            objects_infos[k]["category"] = filename_split[1]
            objects_infos[k]["sub_category"] = filename_split[2]
        else:
            objects_infos[k]["thumbnail"] = False
            objects_infos[k]["category"] = filename_split[0]
            objects_infos[k]["sub_category"] = filename_split[1]
        sub_categories.append(objects_infos[k]["sub_category"])

    # Liste des sub_categories
    dictincts_sub_categories = list(set(sub_categories))

    # Images originales
    original_objects_infos = [
        object_info for object_info in objects_infos if object_info["thumbnail"]
    ]

    stats_report = {}
    for sub_category in dictincts_sub_categories:
        sub_category_objects_infos = [
            object_info
            for object_info in original_objects_infos
            if object_info["sub_category"] == sub_category
        ]
        stats_report.update(
            {
                sub_category: {
                    "count": len(sub_category_objects_infos),
                    "size": sum(
                        [
                            sub_category_object_info["size"]
                            for sub_category_object_info in sub_category_objects_infos
                        ]
                    ),
                }
            }
        )

        # Upload bucket export
        stats_report_byte = json.dumps(stats_report, indent=4).encode("utf-8")
        filename_report = (
            "stats_report_" + datetime.now().strftime("%Y%m%dT%H%M%S") + ".json"
        )
        minio.upload_export(data=stats_report_byte, filename=filename_report)

    # 3.5 Implémentez une fonction qui copie toutes les images
    # vers un nouveau bucket "backup-YYYYMMDD"
    for object_info in list_objects:
        filename: str = object_info["name"]
        image_byte = minio.get_object(
            bucket=minio_config.bucket_images, filename=filename
        )
        minio.create_backup(data=image_byte, prefix=filename.replace(".jpeg", ""))
    backup_created = True

    mongo.close()

    return {
        "total_images": total_images,
        "total_size_kb": total_size_kb,
        "thumbnails_created": thumbnails_created,
        "presigned_url": presigned_url,
        "stats_report": stats_report,
        "backup_created": backup_created,
    }


if __name__ == "__main__":
    results = exercise_3()

    for name, result in results.items():
        print(f"{name}: {result}")
