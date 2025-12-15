use("info");

db.products.drop();
db.createCollection("products");

db.products.insertMany([
    {
        "nom": "Macbook Air",
        "fabriquant": "Apple",
        "prix": 125794.73,
        "ultrabook": true,
        "options": [
            "Intel Core i7",
            "SSD",
            "Long life battery"
        ]
    },
    {
        "nom": "Macbook Pro",
        "fabriquant": "Apple",
        "prix": 13435.99,
        "options": [
            "Intel Core i5",
            "Retina Display",
            "Long Life Battery"
        ]
    },
    {
        "nom": "Thinkpad X230",
        "fabriquant": "Lenovo",
        "prix": 114358.74,
        "ultrabook": true,
        "options": [
            "Intel Core i5",
            "SSD",
            "Long Life Battery"
        ]
    }
]);

// A
db.products.find();

// B
db.products.findOne();

// C
db.products.find({"nom": {$regex: "thinkpad", $options: "i"}});

// D
db.products.find({"prix": {$gte: 13723}});

// E
db.products.findOne({"ultrabook": true});

// F
db.products.findOne({"nom": {$regex: "macbook", $options: "i"}});

// G
db.products.find({"nom": {$regex: "^macbook", $options: "i"}});

// H
db.products.deleteMany({"fabriquant": {$regex: "apple", $options: "i"}});
db.products.find()

// I
db.products.deleteOne({"_id": db.products.findOne({"fabriquant": {$regex: "lenovo", $options: "i"}}, {_id: 1})._id});
db.products.find()