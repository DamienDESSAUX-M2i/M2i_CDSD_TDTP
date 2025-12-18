# Import de la database students.json
# mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo6 --collection=students --file=students.json

from typing import Any

import pymongo

URI = "mongodb://admin:password@localhost:27017/?authSource=admin"


def main() -> None:
    try:
        with pymongo.MongoClient(URI) as client:
            db = client.get_database("exo6")
            collection = db.get_collection("students")

            print("Question 1")
            cursor = collection.find().limit(1)
            print("Document 1 : ", cursor[0])

            print("Question 2")
            result = collection.count_documents({})
            print("Nombre de documents : ", result)

            print("Question 3")
            cursor = collection.find({"name": "Aurelia Menendez"})
            print("name = Aurelia Menendez : ", cursor[0])

            print("Question 4")
            cursor = collection.find({"_id": 50})
            print("_id = 50 : ", cursor[0])

            print("Question 5")
            result = collection.count_documents({"name": ""})
            print("Nombre de name vide : ", result)

            print("Question 6")
            cursor = collection.find().limit(10)
            print(
                "Noms 10 premiers étudiants : ",
                ", ".join([doc["name"] for doc in cursor]),
            )

            print("Question 7")
            cursor = collection.aggregate([{"$limit": 5}, {"$sort": {"name": 1}}])
            print(
                "Noms 5 premiers étudiants triés dans l'ordre croissant : ",
                ", ".join([doc["name"] for doc in cursor]),
            )

            print("Question 8")
            # student0 = collection.find({"_id": 0})
            # doc = cursor[0]
            # for obj in doc["scores"]:
            #     if obj["type"] == "exam":
            #         score_exam = obj["score"]
            student0 = collection.find_one(
                {"_id": 0}, {"scores": {"$elemMatch": {"type": "exam"}}, "_id": 0}
            )
            print("_id = 0, score exam : ", [doc for doc in student0])

            print("Question 9")
            # cursor = collection.find({"_id": 1})
            # doc = cursor[0]
            # scores = [obj["score"] for obj in doc["scores"]]
            # mean = sum(scores) / len(scores)
            mean = collection.aggregate(
                [
                    {"$match": {"_id": 1}},
                    {"$unwind": "$scores"},
                    {"$group": {"_id": "$_id", "avg": {"$avg": "$scores.score"}}},
                ]
            )
            print("_id = 1, moyenne scores : ", [doc for doc in mean])

            print("Question 10")
            cursor = collection.aggregate([{"$unwind": "$scores"}, {"$limit": 5}])
            print("unwind scores + limit 5 : ", [doc for doc in cursor])

            print("Question 11")
            cursor = collection.aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": "$_id",
                            "avg_scores": {"$avg": "$scores.score"},
                        }
                    },
                    {"$sort": {"avg_scores": -1}},
                    {"$limit": 5},
                ]
            )
            print("mean scores par étudiant + limit 5 : ", [doc for doc in cursor])

            print("Question 12")
            cursor = collection.aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": "$scores.type",
                            "avg_scores": {"$avg": "$scores.score"},
                        }
                    },
                    {"$sort": {"avg_scores": -1}},
                ]
            )
            print("mean scores par type : ", [doc for doc in cursor])

            print("Question 13")
            cursor = collection.aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": "$scores.type",
                            "user": {
                                "$top": {
                                    "sortBy": {"scores.score": -1},
                                    "output": "$$ROOT",
                                }
                            },
                        }
                    },
                    {"$project": {"_id": 1, "user.name": 1, "user.scores.score": 1}},
                ]
            )
            print("max score par type : ", [doc for doc in cursor])

            print("Question 14")
            cursor = collection.aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": "$_id",
                            "max_scores": {"$max": "$scores.score"},
                            "min_scores": {"$min": "$scores.score"},
                            "avg_scores": {"$avg": "$scores.score"},
                        }
                    },
                    {"$limit": 1},
                ]
            )
            print("min max avg score par étudiant : ", [doc for doc in cursor])

            print("Question 15")
            cursor = collection.aggregate(
                [
                    {"$unwind": "$scores"},
                    {
                        "$group": {
                            "_id": "$_id",
                            "avg_scores": {"$avg": "$scores.score"},
                        }
                    },
                    {"$match": {"avg_scores": {"$gt": 70}}},
                    {"$count": "total"},
                ]
            )
            print("Nombre étudiant moyenne > 70 : ", [doc for doc in cursor])

            print("Question 16")
            result = collection.update_many(
                {}, [{"$set": {"avg_scores": {"$avg": "$scores.score"}}}]
            )
            cursor = collection.find().limit(1)
            print(
                "Update: moyenne de chaque étudiant : ",
                result.modified_count,
                cursor[0],
            )

            print("Question 17")
            result = collection.update_many(
                {},
                [
                    {
                        "$set": {
                            "level": {
                                "$switch": {
                                    "branches": [
                                        {
                                            "case": {"$gte": ["$avg_scores", 80]},
                                            "then": "Excellent",
                                        },
                                        {
                                            "case": {"$gte": ["$avg_scores", 60]},
                                            "then": "Bien",
                                        },
                                        {
                                            "case": {"$gte": ["$avg_scores", 40]},
                                            "then": "Passable",
                                        },
                                        {
                                            "case": {"$gte": ["$avg_scores", 0]},
                                            "then": "Insuffisant",
                                        },
                                    ],
                                    "default": "Non noté",
                                }
                            }
                        }
                    }
                ],
            )
            cursor = collection.find().limit(1)
            print(
                "Update: moyenne de chaque étudiant : ",
                result.modified_count,
                cursor[0],
            )

            # print("Question 18")
            # min_scores_homework = collection.aggregate(
            #     [
            #         {"$unwind": "$scores"},
            #         {"$match": {"scores.type": "homework"}},
            #         {
            #             "$group": {
            #                 "_id": "$_id",
            #                 "min_homework": {"$min": "$scores.score"},
            #             }
            #         },
            #     ]
            # )
            # for doc in min_scores_homework:
            #     collection.update_one(
            #         {"_id": doc["_id"]},
            #         {
            #             "$pull": {
            #                 "scores": {
            #                     "type": "homework",
            #                     "score": doc["min_homework"],
            #                 }
            #             }
            #         },
            #     )
            # cursor = collection.find().limit(1)
            # print(
            #     "Update name _id 113 : ",
            #     cursor[0],
            # )

            print("Question 19")
            result = collection.update_one(
                {"_id": 113},
                {"$set": {"name": "Nom inconnu"}},
            )
            cursor = collection.find({"_id": 113})
            print(
                "Update name _id 113 : ",
                result.modified_count,
                cursor[0],
            )

    except Exception as e:
        print(f"Connecting failled : {e}")


if __name__ == "__main__":
    main()
