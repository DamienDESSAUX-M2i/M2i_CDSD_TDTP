// Import de la database livres.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo4 --collection=restaurants --file=restaurants.json --jsonArray

// 1
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    }
]);

// 2
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $sort: {
            "name": 1
        }
    }
]);

// 3
use("exo4");
db.restaurants.aggregate([
    {
        $match: {
            "borough": {$regex: "Brooklyn", $options: "i"}
        }
    },
    {
        $limit: 10
    },
    {
        $sort: {
            "name": 1
        }
    }
]);

// 4
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $project: {
            "name": 1,
            "borough": 1
        }
    }
]);

// 5
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $project: {
            "address": 0,
            "grades": 0
        }
    }
]);

// 6
use("exo4");
data = db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $addFields: {
            "nb_grades": {$size: "$grades"}
        }
    }
]);

// 7
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $addFields: {
            "nb_grades": {$size: "$grades"}
        }
    },
    {
        $sort: {
            "new_rating": -1
        }
    }
]);

// 8
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $project: {
            "name": {$toUpper: "$name"},
            "borough": {$toUpper: "$borough"}
        }
    }
]);

// 9
use("exo4");
db.restaurants.aggregate([
    {
        $limit: 10
    },
    {
        $project: {
            "name": {$toUpper: "$name"},
            "borough": {$substr: ["$borough", 0, 3]}
        }
    }
]);

// 10
use("exo4");
db.restaurants.aggregate([
    {
        $count: "nb_restaurants"
    }
]);

// 11
use("exo4");
db.restaurants.aggregate([
    {
        $group: {
            "_id": "$borough",
            "nb_restaurants": {$sum: 1}
        },
    },
    {
        $project: {
            "square": "$_id",
            "_id": 0,
            "nb_restaurants": 1
        }
    }
]);
