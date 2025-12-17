// Import de la database livres.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo5 --collection=gymnases --file=gymnases.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo5 --collection=sportifs --file=sportifs.json

use("exo5");

db.gymnases.find().limit(5);
db.sportifs.find().limit(5);

// 1
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            "Age": {$gt: 20, $lt: 30}
        }
    },
    {
        $project: {
            "_id": 1,
            "Nom": 1,
            "Prenom": 1
        }
    }
]);

// 2
use("exo5");
db.gymnases.aggregate([
    {
        $match: {
            "Ville": {$in: ["VILLETANEUSE", "SARCELLES"]},
            "Surface": {$gt: 200}
        }
    }
]);

// 3
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            "Sports.Jouer": "Hand ball"
        }
    },
    {
        $project: {
            "_id": 0,
            "Nom": 1
        }
    }
]);

// 4
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            "Sports.Jouer": null
        }
    },
    {
        $project: {
            "_id": 0,
            "Nom": 1,
            "IdSportif": 1
        }
    }
]);

// 5
use("exo5");
db.gymnases.aggregate([
    {
        $match: {
            "Seances.Jour": {$ne: "dimanche"}
        }
    },
    {
        $count: "nb"
    }
]);
use("exo5");
db.gymnase.aggregate([
    {
        $match: {
            "Seances": {
                $not: {
                    $elemMatch: {
                        "Jour": "dimanche"
                    }
                }
            }
        }
    },
    {
        $count: "nb"
    }
]);

// 6
use("exo5");
db.gymnases.aggregate([
    {
        $match: {
            "Seances": {
                $not: {
                    $elemMatch: {
                        "Libelle": { $nin: ["Basket ball", "Volley ball"] }
                    }
                }
            }
        }
    }
]);

// 7
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            $and: [
                {"Sports.Jouer": {$exists: true}},
                {"Sports.Entrainer": {$exists: true}}
            ]
        }
    },
    {
        $addFields: {
            "entrainerArray": {
                $cond: {
                    if: { $isArray: "$Sports.Entrainer" },
                    then: "$Sports.Entrainer",
                    else: [ "$Sports.Entrainer" ]
                }
            }
        },
    },
    {
        $addFields: {
            "jouerArray": {
                $cond: {
                    if: { $isArray: "$Sports.Jouer" },
                    then: "$Sports.Jouer",
                    else: [ "$Sports.Jouer" ]
                }
            }
        },
    },
    {
        $match: {
            $expr: {
                $setIsSubset: ["$entrainerArray", "$jouerArray"]
            }
        }
    }
]);


// 8
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            "Nom": "KERVADEC"
        }
    },
    {
        $lookup: {
            from: "sportifs",
            localField: "IdSportifConseiller",
            foreignField: "IdSportif",
            as: "SportifConseiller"
        }
    },
    {
        $project: {
            "Nom": 1,
            "SportifConseiller.Nom": 1
        }
    }
]);

// 9
use("exo5");
db.sportifs.aggregate([
    {
        $match: {
            "Sports.Jouer": {
                $regex: "basket", $options: "i"
            }
        }
    },
    {
        $group: {
            "_id": null,
            "AvgAge": {
                $avg: "$Age"
            }
        }
    }
]);

// 10
use("exo5");
db.sportifs.aggregate([
    {
        $addFields: {
            "entrainerArray": {
                $cond: {
                    if: { $isArray: "$Sports.Entrainer" },
                    then: "$Sports.Entrainer",
                    else: [ "$Sports.Entrainer" ]
                }
            }
        }
    },
    {
        $match: {
            $expr: {
                $setIsSubset: ["$entrainerArray", ["Hand ball", "Basket ball"]]
            }
        }
    }
]);

// 11
use("exo5");
db.sportifs.aggregate([
    {
        $unwind: "$Sports.Arbitrer"
    },
    {
        $group: {
            "_id": {
                "IdSportif": "$IdSportif",
                "Nom": "$Nom",
            },
            "NombreSportsArbitrer": {
                $sum: 1
            }
        }
    },
    {
        $sort: {
            "NombreSportsArbitrer": -1
        }
    },
    {
        $project: {
            "_id": 0,
            "IdSportif": "$_id.IdSportif",
            "Nom": "$_id.Nom",
            "NombreSportsArbitrer": 1
        }
    }
]);
