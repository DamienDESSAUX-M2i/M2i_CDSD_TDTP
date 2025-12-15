use("biblio");

// Sélectionne les 5 premiers livres
db.books.find().limit(5);

// Sélection des livres ayant exactement 2 auteurs
db.books.find({authors: {$size: 2}});

// Compter le nombre de livre vérifiant une condition
db.books.find({"authors": {$size: 2}}).count(); // déprécié
db.books.countDocuments({authors: {$size: 2}});

// Sélection des livres ayant au moins 400 pages
db.books.find({"pageCount": {$gte: 400}});

// Sélection des livres ayant pour id soit 55, soit 75
db.books.find({_id: {$in: [55, 75]}});

// Trier les livres
// 1 -> croissant
// -1 -> décroissant
db.books.find({authors: {$size: 2}}).sort({title: 1, _id: -1});

// Opérateur logique
// $and -> et logique
// $or -> ou logique
db.books.find({$and: [{_id: {$gt: 25}}, {_id: {$lt: 28}}]});

// Sélection des champs _id et authors
db.books.find({_id: {$gt: 25}}, {_id: 1, authors: 1});

// slice -> sélection de l'objet 1
db.books.find({_id: {$lte:5}}, {authors: {$slice: 1}, title:1});

// Sélection par regex
// $option: i -> ignorer la casse
db.books.find({longDescription: {$regex: "Distributed", $option: "i"}});