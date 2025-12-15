// Import de la database users.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo2 --collection=users --file=users.json

use("exo2");

// Question 1
// db.users.insertOne({
//     "name": "Chuck Norris",
//     "age": 77,
//     "hobbies": ["Karate", "Kung-fu", "Ruling the world"]
// });

// Question 2
db.users.find({"name": "Chuck Norris"});

db.users.find({"name": "Chuck Norris"}, {"_id": 0});

db.users.find({"age": {$gte: 20, $lte: 25}});

db.users.find({"age": {$gte: 20, $lte: 25}, "gender": "male"});

db.users.find({"address.state": "Louisiana"});

db.users.find().sort({"age": -1}).limit(5);

db.users.countDocuments({"age": 30, "gender": "female"});

// Question 3
db.users.updateMany({}, {$unset: {"phone": 1}});
db.users.find().limit(5);

db.users.updateOne({"name": "Chuck Norris"}, {$set: {"age": "infinity"}});
db.users.find({"name": "Chuck Norris"});

db.users.updateMany({"age": {$gte: 50}}, {$push: {"hobbies": "jardinage"}});
db.users.find({"age": {$gte: 50}});