use("hopital");

db.patient.drop();

db.patient.insertMany([
    {
        "firstname": "Alice",
        "lastname": "A",
        "age": 30,
        "history": [
            {
                "desease": "rhume",
                "treatment": "sirop"
            },
            {
                "desease": "grippe",
                "treatment": "anti-biotique"
            }
        ]
    },
    {
        "firstname": "Bob",
        "lastname": "B",
        "age": 40,
        "history": [
            {
                "desease": "rhume",
                "treatment": "sirop"
            }
        ]
    },
    {
        "firstname": "Oscar",
        "lastname": "O",
        "age": 50,
        "history": [
            {
                "desease": "rhume",
                "treatment": "sirop"
            },
            {
                "desease": "grippe",
                "treatment": "anti-biotique"
            },
            {
                "desease": "angine",
                "treatment": "anti-biotique"
            }
        ]
    }
]);

db.patient.updateOne(
    {"firstname": "Oscar", "lastname": "O"},
    {
        $set: {"age": 20, "firstname": "Cesar", "lastname": "C"},
        $push:{"history": {"desease" : "otite", "treatment": "anti-biotique"}}
    }
);

db.patient.find({"age": {$gt: 29}});

db.patient.find({"firstname": "Alice"});

db.patient.deleteMany({"history.desease": "rhume"});