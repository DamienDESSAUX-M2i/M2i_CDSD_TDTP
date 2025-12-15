// Connexion db "demo"
use("demo");

// Update le prix de la donnée d'id 1
db.products.find({id: 1})
db.products.updateOne({id: 1}, {$set: {price: 10124}})
db.products.find({id: 1})