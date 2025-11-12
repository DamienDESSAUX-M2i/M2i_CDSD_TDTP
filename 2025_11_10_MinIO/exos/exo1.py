import os
from lorem_text import lorem
from minio import Minio
from minio.commonconfig import CopySource


def generate_file(file_path) -> None:
    with open(file_path, "wt", encoding="utf-8") as f:
        f.write(lorem.sentence())
        f.write(lorem.sentence())
        f.write(lorem.sentence())


def main() -> None:
    # Question 1
    print("Création d'un client.")
    client = Minio(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Question 2
    bucket_name = "bucket1"
    print(f"Création du bucket {bucket_name}.")
    if client.bucket_exists(bucket_name=bucket_name):
        print(f"{bucket_name} already exists.")
    else:
        client.make_bucket(bucket_name=bucket_name)
        print(f"{bucket_name} maked.")
    
    # Question 3
    file_path = "./2025_11_10_MinIO/exos/file1.txt"
    print(f"Génération du fichier {file_path}")
    generate_file(file_path=file_path)

    # Question 4
    object_name = "file1.txt"
    print(f"Téléchargement du fichier {file_path} dans le bucket {bucket_name}.")
    client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=file_path
        )
    print(f"{file_path} puted in {bucket_name}.")

    # Question 5
    print(f"Affichage de la liste des objets du bucket {bucket_name}.")
    for object in client.list_objects(bucket_name=bucket_name):
        print(object.object_name)

    # Question 6
    copy_source = CopySource(
        bucket_name=bucket_name,
        object_name=object_name
        )
    object_name_copy = "file1_copy.txt"
    print(f"Copie de l'objet {object_name} en {object_name_copy}")
    client.copy_object(bucket_name=bucket_name, object_name=object_name_copy, source=copy_source)

    # Question 7
    copy_source = CopySource(
        bucket_name=bucket_name,
        object_name=object_name
        )
    object_name_rename = "file2.txt"
    print(f"Renommage de l'objet {object_name} en {object_name_rename}")
    client.copy_object(bucket_name=bucket_name, object_name=object_name_rename, source=copy_source)
    client.remove_object(bucket_name=bucket_name, object_name=object_name)

    # Question 8
    print(f"Récupération de l'objet {object_name_rename}")
    response = client.get_object(bucket_name=bucket_name, object_name=object_name_rename)
    print(response.data)
    response.close()
    response.release_conn()

    # Question 9
    print(f"Suppression des objets {object_name_copy} et {object_name_rename}.")
    client.remove_objects(bucket_name=bucket_name, delete_object_list=[object_name_rename, object_name_copy])

    # Question 10
    print(f"Suppression du fichier local {file_path}.")
    os.remove(file_path)



if __name__ == "__main__":
    main()