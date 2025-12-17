// Import de la database livres.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=resto --collection=restaurants --file=restaurants.json

use("resto");
db.restaurants.find().limit(5);

use("resto");
db.restaurants.find({postcode: {$not: {$eq: "8NX"}}});

use("resto");
db.restaurants.aggregate([
    { // WHERE
        $match: {"rating": 5}
    },
    { // fonction d'aggrégation
        $count: "comptage"
    }
]);
// [
//   {
//     "comptage": 1107
//   }
// ]

use("resto");
db.restaurants.aggregate([
    { // WHERE
        $match: {"rating": 5}
    },
    { // filtrer colonnes
        $project: {"URL": 1, "name": 1}
    }
]);
// [
//   {
//     "_id": {
//       "$oid": "55f14312c7447c3da7051b26"
//     },
//     "URL": "http://www.just-eat.co.uk/restaurants-cn-chinese-cardiff/menu",
//     "name": ".CN Chinese"
//   },
//   ...
// ]

use("resto");
db.restaurants.aggregate([
    { // GROUPBY
        $group: {
            "_id": "$type_of_food",
            "count": {$sum: 1}
        }
    }
]);
// [
//   {
//     "_id": "Pasta",
//     "count": 1
//   },
//   ...
// ]

use("resto");
db.restaurants.aggregate([
    { // GROUP BY
        $group: {
            "_id": "$type_of_food",
            "count": {$sum: 1}
        }
    },
    { // HAVING
        $match: {
            "count": {$gte: 10}
        }
    },
    { // ORDER BY
        $sort: {"count": -1}
    }
]);

use("resto");
db.restaurants.aggregate([
    { // GROUP BY
        $group: {
            "_id": "$type_of_food",
            "note_moyenne": {$avg: "$rating"}
        }
    },
    { // ORDER BY
        $sort: {"note_moyenne": -1}
    }
]);
// [
//   {
//     "_id": "Punjabi",
//     "note_moyenne": 6
//   },
//   ...
// ]

use("resto");
db.restaurants.aggregate([
    { // WHERE
        $match: {
            "rating": {$ne: "Not yet rated"}
        }
    },
    { // GROUP BY
        $group: {
            "_id": "$type_of_food",
            "total_rating": {$sum: 1},
            "avg_rating": {$avg: "$rating"}
        }
    }
]);
// [
//   {
//     "_id": "Azerbaijan",
//     "total_rating": 6,
//     "avg_rating": 5
//   },
//   ...
// ]