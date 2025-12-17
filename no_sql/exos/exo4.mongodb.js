// Import de la database livres.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo3 --collection=livres --file=livres.json --jsonArray

use("exo3");
db.livres.find().limit(5);

// 1
use("exo3");
db.livres.aggregate([
    {
        $match: {
            "authors": "Toru Ishida"
        }
    },
    {
        $sort: {
            "title": 1,
            "pages.start": 1
        }
    }
]);

// 2
use("exo3");
db.livres.aggregate([
    {
        $match: {
            "authors": "Toru Ishida"
        }
    },
    {
        $sort: {
            "title": 1,
            "pages.start": 1
        }
    },
    {
        $project: {
            "title": 1,
            "pages": 1
        }
    }
]);

// 3
use("exo3");
db.livres.aggregate([
    {
        $match: {
            "authors": "Toru Ishida"
        }
    },
    {
        $count: "nb_publication"
    }
]);

// 4
use("exo3");
db.livres.aggregate([
    {
        $match: {
            "year": {$gte: 2011}
        }
    },
    {
        $group: {
            "_id": "$type",
            "nb_publication": {$sum: 1}
        }
    }
]);

// 5
use("exo3");
db.livres.aggregate([
    {
        $unwind: "$authors"
    },
    {
        $group: {
            "_id": "$authors",
            "nb_publication": {$sum: 1}
        }
    },
    {
        $sort: {
            "nb_publication": -1
        }
    }
]);