use("ManyToMany");

db.createCollection("orders");
db.createCollection("products");

db.products.insertMany([
    {
        name : "Clavier",
        orders : []
    },
    {
        name : "souris",
        orders : []
    }
]);
db.orders.insertMany([
    {
        company : "Apple",
        products : []
    },
    {
        compagny : "Sony",
        products : []
    }
]);

db.products.find();
db.orders.find();

db.orders.updateOne(
    {
        _id : ObjectId("69416f892238267d1ea50789")
    },
    {
        $push : {
            products : ObjectId("69416f83cdc5b34203faf019")
        }
    }
);
db.orders.updateOne(
    {
        _id : ObjectId("69416f892238267d1ea50789")},
        {$push : {
            products : ObjectId("69416f83cdc5b34203faf01a")
        }
    }
);
db.orders.updateOne(
    {
        _id : ObjectId("69416f892238267d1ea5078a")},
        {$push : {
            products : ObjectId("69416f83cdc5b34203faf019")
        }
    }
);
db.orders.updateOne(
    {
        _id : ObjectId("69416f892238267d1ea5078a")},
        {$push : {
            products : ObjectId("69416f83cdc5b34203faf01a")
        }
    }
);

db.products.updateOne(
    {
        _id : ObjectId("69416f83cdc5b34203faf019")},
        {$push :{
            orders : ObjectId("69416f892238267d1ea50789")
        }
    }
);
db.products.updateOne(
    {
        _id : ObjectId("69416f83cdc5b34203faf019")},
        {$push :{
            orders : ObjectId("69416f892238267d1ea5078a")
        }
    }
);
db.products.updateOne(
    {
        _id : ObjectId("69416f83cdc5b34203faf01a")},
        {$push :{
            orders : ObjectId("69416f892238267d1ea50789")
        }
    }
);
db.products.updateOne(
    {
        _id : ObjectId("69416f83cdc5b34203faf01a")},
        {$push: {
            orders : ObjectId("69416f892238267d1ea5078a")
        }
    }
);

db.products.aggregate(
    {
        $lookup : {
            from: "orders",
            localField : "orders",
            foreignField : "_id",
            as: "orders"
        }
    }
);
