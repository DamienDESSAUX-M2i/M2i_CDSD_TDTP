from src.storage import MongoDBStorage


def exercise_2():
    mongo = MongoDBStorage()

    # 2.1 Trouvez tous les laptops avec un prix < 500$
    cheap_laptops = mongo.get_cheap_laptops()

    # 2.2 Trouvez le produit le plus cher de chaque catégorie
    # Indice: utilisez $group avec $max et $first
    most_expensive_by_cat = mongo.get_most_expensive_by_cat()

    # 2.3 Calculez le prix moyen des produits avec rating >= 4
    avg_price_good_rating = mongo.get_avg_price_good_rating(rating=4)

    # 2.4 Trouvez les produits dont le titre contient "Samsung" ou "Apple"
    # Indice: utilisez $regex ou $in
    brand_products = mongo.get_brand_products(text_inside=["Samsung", "Apple"])

    # 2.5 Créez un classement des produits par rapport qualité/prix
    # Score = rating / (price / 100)
    # Retournez le top 10
    value_ranking = mongo.get_value_ranking()

    # 2.6 Groupez les produits par tranche de prix (0-200, 200-500, 500-1000, 1000+)
    # et comptez le nombre de produits par tranche
    price_ranges = mongo.get_price_ranges()

    # 2.7 Trouvez les produits qui ont le même prix (doublons de prix)
    # Indice: $group puis $match sur count > 1
    same_price_products = mongo.get_same_price_products()

    mongo.close()

    return {
        "cheap_laptops": cheap_laptops,
        "most_expensive_by_cat": most_expensive_by_cat,
        "avg_price_good_rating": avg_price_good_rating,
        "brand_products": brand_products,
        "value_ranking": value_ranking,
        "price_ranges": price_ranges,
        "same_price_products": same_price_products,
    }


if __name__ == "__main__":
    results = exercise_2()

    for name, result in results.items():
        print(f"\n{'=' * 50}")
        print(f"{name}:")
        print(f"{'=' * 50}")

        if isinstance(result, list):
            for item in result[:5]:  # Limiter l'affichage
                print(item)
            if len(result) > 5:
                print(f"... et {len(result) - 5} autres")
        else:
            print(result)
