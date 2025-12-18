from datetime import datetime

import pymongo

URI = "mongodb://admin:password@localhost:27017/?authSource=admin"


def main() -> None:
    try:
        print(f"Attempting connecxion : {URI}.")
        with pymongo.MongoClient(URI) as client:
            print("Connected successfully.")

            db = client.get_database("demo_crud")
            # <=> db = client["demo_crud"]
            collection = db.get_collection("utilisateurs")
            # <=> collection = db["utilisateurs"]

            collection.drop()

            # Insertion
            print("Attempting insertion : Documents.")
            collection.insert_many(
                [
                    {
                        "nom": "Dupont",
                        "prenom": "Jean",
                        "age": 30,
                        "ville": "Paris",
                        "profession": "Développeur",
                        "date_creation": datetime.now(),
                    },
                    {
                        "nom": "Martin",
                        "prenom": "Marie",
                        "age": 25,
                        "ville": "Lyon",
                        "profession": "Designer",
                        "date_creation": datetime.now(),
                    },
                    {
                        "nom": "Dubois",
                        "prenom": "Pierre",
                        "age": 40,
                        "ville": "Marseille",
                        "profession": "Manager",
                        "date_creation": datetime.now(),
                    },
                ]
            )
            print("Inserted successfully.")

            # Lecture
            print("Attempting select : Documents.")
            for user in collection.find():
                print(user)

            for user in collection.find({"age": {"$lt": 30}}):
                print(
                    f"Firstname : {user['prenom']}, Lastname : {user['nom']}, Age : {user['age']}years."
                )

            # Update
            print("Attempting select : Documents.")
            result = collection.update_one(
                {"nom": "Dupont", "prenom": "Jean"}, {"$set": {"age": 31}}
            )
            print(f"Number of modified document : {result.modified_count}")

            # Delete
            print("Attempting delete : Documents.")
            result = collection.delete_many({"age": {"$gt": 35}})
            print(f"Number of deleted document : {result.deleted_count}")

    except Exception as e:
        print(f"Connecting failled : {e}")


if __name__ == "__main__":
    main()
