// Connexion db "demo"
use("demo");

// Sélectionner les produits de catégorie "Electronics"
db.products.find({category: "Electronics"});

// Sélectionner les produits disponibles et de catégorie "Electronics"
db.products.find({available: true}, {category: "Electronics"});

// Sélectionner les produits dont le prix est compris entre 100 et 500
db.products.find({price: {$gt: 100, $lt: 500}});

// Sélectionner les produits dont la catégorie est dans une liste
db.products.find({category: {$in: ["Electronics", "Audio"]}});

// Sélectionner les produits dont l'un des tags est "drone"
db.products.find({tags: "drone"})

// Sélectionner les produits dont l'un des commentaires est écrit par le user "Alice"
db.products.find({"comments.user": "Alice"})