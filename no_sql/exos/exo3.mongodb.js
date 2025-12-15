// Import de la database livres.json
// mongoimport --uri="mongodb://admin:password@localhost:27017/?authSource=admin" --db=exo3 --collection=livres --file=livres.json --jsonArray

use("exo3");

db.livres.find().limit(5);

db.livres.distinct("type");
// [
//   "Article",
//   "Book",
//   "Phd"
// ]

db.livres.find({"type": "Book"});

db.livres.find({"type": "Article", "year": {$gte: 2011}});

db.livres.find({"type": "Book", "year": {$gte: 2014}});

db.livres.find({"type": "Article", "authors": "Toru Ishida"});

db.livres.distinct("publisher");

db.livres.distinct("authors");
