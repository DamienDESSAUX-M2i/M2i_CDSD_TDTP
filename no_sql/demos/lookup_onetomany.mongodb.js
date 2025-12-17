use("OneToMany");

db.createCollection("users");
db.createCollection("addresses");

db.users.insertOne({
    "name": "Clément",
    "age": 30
});
// L'utilisateur inséré a pour id "694167c921b5364003154de1"
// On crée une adresse
// et on ajoute une clé étrangère "user_id" qui a pour valeur "ObjectId("694167c921b5364003154de1")"
db.addresses.insertOne({
    "street": "rue des coquilles",
    "number": 10,
    "city": "Lille",
    "user_id": ObjectId("694167c921b5364003154de1")
});

db.users.find();
db.addresses.find();

// Jointure
db.users.aggregate([
    {
        $lookup: {
            from: "addresses",
            localField: "_id",
            foreignField: "user_id",
            as: "addresses"
        }
    }
]);
