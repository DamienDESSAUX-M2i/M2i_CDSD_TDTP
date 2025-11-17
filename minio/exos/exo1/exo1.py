import os
from lorem_text import lorem
from minio import Minio
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject


def generate_file(file_path) -> None:
    with open(file_path, "wt", encoding="utf-8") as f:
        f.write(lorem.sentence())
        f.write(lorem.sentence())
        f.write(lorem.sentence())


def main() -> None:
    # Question 1
    print("1. Création d'un client.")
    client = Minio(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Question 2
    bucket_name = "bucket1"
    print(f"2.Création du bucket {bucket_name}.")
    if client.bucket_exists(bucket_name=bucket_name):
        print(f"\t{bucket_name} already exists.")
    else:
        client.make_bucket(bucket_name=bucket_name)
        print(f"\t{bucket_name} maked.")
    
    # Question 3
    file_path = "./minio/exos/exo1/file1.txt"
    print(f"3. Génération du fichier {file_path}")
    generate_file(file_path=file_path)

    # Question 4
    object_name = "file1.txt"
    print(f"4.Téléchargement du fichier {file_path} dans le bucket {bucket_name}.")
    client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path
        )
    print(f"\t{file_path} puted in {bucket_name}.")

    # Question 5
    print(f"5. Affichage de la liste des objets du bucket {bucket_name}.")
    for object in client.list_objects(bucket_name=bucket_name):
        print(object.object_name)

    # Question 6
    copy_source = CopySource(
        bucket_name=bucket_name,
        object_name=object_name
        )
    object_name_copy = "file1_copy.txt"
    print(f"6. Copie de l'objet {object_name} en {object_name_copy}")
    client.copy_object(bucket_name=bucket_name, object_name=object_name_copy, source=copy_source)

    # Question 7
    copy_source = CopySource(
        bucket_name=bucket_name,
        object_name=object_name
        )
    object_name_rename = "file2.txt"
    print(f"7. Renommage de l'objet {object_name} en {object_name_rename}")
    client.copy_object(bucket_name=bucket_name, object_name=object_name_rename, source=copy_source)
    client.remove_object(bucket_name=bucket_name, object_name=object_name)

    # Question 8
    print(f"8. Récupération de l'objet {object_name_rename}")
    file_path_get = "./2025_11_10_MinIO/exos/exo1/file_get.txt"
    client.fget_object(bucket_name=bucket_name, object_name=object_name_rename, file_path=file_path_get)

    response = client.get_object(bucket_name=bucket_name, object_name=object_name_rename)
    print(f"{response.data}")
    response.close()
    response.release_conn()

    # Question 9
    print(f"9. Suppression des objets {object_name_copy} et {object_name_rename}. Suppression du bicket {bucket_name}.")
    delete_object_list = [
        DeleteObject(name=object_name_rename),
        DeleteObject(name=object_name_copy)
        ]
    errors = client.remove_objects(bucket_name=bucket_name, delete_object_list=delete_object_list)
    for error in errors:
        print("error occured when deleting object", error)
    client.remove_bucket(bucket_name=bucket_name)

    # Question 10
    print(f"10. Suppression du fichier local {file_path}.")
    os.remove(file_path)
    os.remove(file_path_get)



if __name__ == "__main__":
    main()