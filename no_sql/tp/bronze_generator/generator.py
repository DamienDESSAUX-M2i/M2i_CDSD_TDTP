import random
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:admin123@localhost:27017/')

client = MongoClient(MONGO_URI)
db = client['bronze_db']

customers_collection = db['customers']
transactions_collection = db['transactions']
campaigns_collection = db['campaigns']

first_names = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Emma', 'Thomas', 'Julie', 'Marc', 'Laura', 
               'Nicolas', 'Camille', 'Alexandre', 'Sarah', 'David', 'Léa', 'Julien', 'Manon']
last_names = ['Dupont', 'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Petit', 'Richard', 
              'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel']
domains = ['gmail.com', 'yahoo.fr', 'hotmail.com', 'outlook.fr', 'orange.fr']
countries = ['France', 'Belgique', 'Suisse', 'Canada', 'Luxembourg']
cities = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 
          'Bordeaux', 'Lille', 'Rennes', 'Reims', 'Toulon', 'Grenoble', 'Dijon']
products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch', 'Camera', 'Monitor', 
            'Keyboard', 'Mouse', 'Printer', 'Router', 'Speaker', 'Console', 'TV']
campaign_types = ['Email', 'Social Media', 'Display', 'Search', 'Video', 'Influencer']
campaign_names = ['Summer Sale', 'Black Friday', 'New Product Launch', 'Newsletter', 
                  'Retargeting', 'Brand Awareness', 'Holiday Special', 'Flash Sale']

def generate_customer():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    customer = {
        'customer_id': f"CUST{random.randint(10000, 99999)}",
        'created_at': datetime.now() - timedelta(days=random.randint(0, 730))
    }
    
    if random.random() > 0.15:
        customer['first_name'] = first_name
    
    if random.random() > 0.15:
        customer['last_name'] = last_name
    
    if random.random() > 0.20:
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@{random.choice(domains)}"
        customer['email'] = email
    
    if random.random() > 0.25:
        customer['age'] = random.randint(18, 75)
    
    if random.random() > 0.30:
        customer['phone'] = f"+33{random.randint(600000000, 799999999)}"
    
    if random.random() > 0.20:
        customer['country'] = random.choice(countries)
    
    if random.random() > 0.35:
        customer['city'] = random.choice(cities)
    
    if random.random() > 0.40:
        customer['postal_code'] = f"{random.randint(10000, 99999)}"
    
    if random.random() > 0.50:
        customer['gender'] = random.choice(['M', 'F', 'Other'])
    
    if random.random() > 0.60:
        customer['marketing_consent'] = random.choice([True, False])
    
    return customer

def generate_transaction():
    transaction = {
        'transaction_id': f"TXN{random.randint(100000, 999999)}",
        'timestamp': datetime.now() - timedelta(days=random.randint(0, 365))
    }
    
    if random.random() > 0.10:
        transaction['customer_id'] = f"CUST{random.randint(10000, 99999)}"
    
    if random.random() > 0.15:
        transaction['product'] = random.choice(products)
    
    if random.random() > 0.10:
        transaction['amount'] = round(random.uniform(10, 2000), 2)
    
    if random.random() > 0.25:
        transaction['quantity'] = random.randint(1, 5)
    
    if random.random() > 0.30:
        transaction['payment_method'] = random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'])
    
    if random.random() > 0.35:
        transaction['status'] = random.choice(['Completed', 'Pending', 'Cancelled', 'Refunded'])
    
    if random.random() > 0.40:
        transaction['discount_applied'] = round(random.uniform(0, 50), 2)
    
    if random.random() > 0.45:
        transaction['shipping_cost'] = round(random.uniform(0, 25), 2)
    
    return transaction

def generate_campaign():
    campaign = {
        'campaign_id': f"CAMP{random.randint(1000, 9999)}",
        'start_date': datetime.now() - timedelta(days=random.randint(0, 180))
    }
    
    if random.random() > 0.15:
        campaign['campaign_name'] = random.choice(campaign_names)
    
    if random.random() > 0.15:
        campaign['campaign_type'] = random.choice(campaign_types)
    
    if random.random() > 0.20:
        campaign['budget'] = round(random.uniform(1000, 50000), 2)
    
    if random.random() > 0.25:
        campaign['impressions'] = random.randint(1000, 500000)
    
    if random.random() > 0.30:
        campaign['clicks'] = random.randint(50, 25000)
    
    if random.random() > 0.35:
        campaign['conversions'] = random.randint(5, 2000)
    
    if random.random() > 0.40:
        campaign['spend'] = round(random.uniform(500, 45000), 2)
    
    if random.random() > 0.45:
        campaign['target_audience'] = random.choice(['18-25', '26-35', '36-45', '46-55', '55+'])
    
    if random.random() > 0.50:
        campaign['status'] = random.choice(['Active', 'Paused', 'Completed', 'Draft'])
    
    return campaign

def main():
    print("Génération de données marketing dans MongoDB Bronze...")
    
    customers_collection.drop()
    transactions_collection.drop()
    campaigns_collection.drop()
    
    batch_size = 100
    total_customers = 5000
    total_transactions = 15000
    total_campaigns = 200
    
    print(f"Insertion de {total_customers} clients...")
    for i in range(0, total_customers, batch_size):
        customers = [generate_customer() for _ in range(min(batch_size, total_customers - i))]
        customers_collection.insert_many(customers)
        print(f"  {i + len(customers)}/{total_customers} clients insérés")
    
    print(f"Insertion de {total_transactions} transactions...")
    for i in range(0, total_transactions, batch_size):
        transactions = [generate_transaction() for _ in range(min(batch_size, total_transactions - i))]
        transactions_collection.insert_many(transactions)
        print(f"  {i + len(transactions)}/{total_transactions} transactions insérées")
    
    print(f"Insertion de {total_campaigns} campagnes...")
    for i in range(0, total_campaigns, batch_size):
        campaigns = [generate_campaign() for _ in range(min(batch_size, total_campaigns - i))]
        campaigns_collection.insert_many(campaigns)
        print(f"  {i + len(campaigns)}/{total_campaigns} campagnes insérées")
    
    print("\nGénération terminée!")
    print(f"Total: {customers_collection.count_documents({})} clients, "
          f"{transactions_collection.count_documents({})} transactions, "
          f"{campaigns_collection.count_documents({})} campagnes")

if __name__ == '__main__':
    time.sleep(10)
    main()
