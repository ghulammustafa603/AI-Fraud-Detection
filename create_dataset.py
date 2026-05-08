import pandas as pd
import random
from datetime import datetime, timedelta
from model import calculate_risk

def generate_large_dataset(n=100000):
    """Generates a massive Kaggle-style dataset for model evaluation."""
    data = []
    cities = ["Karachi", "Lahore", "Faisalabad", "Peshawar", "Quetta", "Multan"]
    wallets = ["JazzCash", "Easypaisa"]
    types = ["TRANSFER", "CASH_OUT", "PAYMENT", "CASH_IN"]
    
    start_date = datetime.now() - timedelta(days=60)
    
    print(f"Generating {n} transactions... This may take a few seconds.")
    
    for i in range(n):
        is_fraud_scenario = random.random() < 0.08 # Real-world fraud is usually rare
        
        # Balance logic
        old_balance = random.randint(500, 200000)
        
        if is_fraud_scenario:
            # Ensure old_balance is sufficient for a 'large' fraud amount, or scale the fraud amount down
            upper_limit = min(100000, old_balance + 5000)
            lower_limit = 20000
            
            if lower_limit >= upper_limit:
                # If balance is too low for a 20k fraud, we adjust the balance to simulate a high-value account
                old_balance = random.randint(25000, 200000)
                upper_limit = min(100000, old_balance + 5000)
            
            amount = random.randint(lower_limit, upper_limit)
            hour = random.choice([0, 1, 2, 3, 4, 5])
            is_new_device = random.choice([True, False, True])
            is_loc_mismatch = random.choice([True, False, True])
            high_freq = random.choice([True, False])
            age = random.choice([16, 72, 25])
            tx_type = random.choice(["TRANSFER", "CASH_OUT"])
        else:
            amount = random.randint(100, 15000)
            hour = random.randint(7, 23)
            is_new_device = False
            is_loc_mismatch = False
            high_freq = False
            age = random.randint(20, 50)
            tx_type = random.choice(types)

        new_balance = old_balance - amount if tx_type != "CASH_IN" else old_balance + amount
        tx_time = start_date + timedelta(seconds=random.randint(0, 5184000))
        tx_time = tx_time.replace(hour=hour)
        
        tx = {
            "step": i // 24, # Simulate hours passing
            "type": tx_type,
            "amount": amount,
            "wallet": random.choice(wallets),
            "city": random.choice(cities),
            "oldbalanceOrg": old_balance,
            "newbalanceOrig": new_balance,
            "is_new_device": is_new_device,
            "is_loc_mismatch": is_loc_mismatch,
            "high_freq": high_freq,
            "user_age": age,
            "time": tx_time
        }
        
        # Ground truth scoring
        score, _ = calculate_risk(tx)
        tx['risk_score'] = score
        tx['is_fraud'] = 1 if score > 70 else 0
        
        data.append(tx)
        
        if i % 20000 == 0:
            print(f"Progress: {i}/{n}")
            
    df = pd.DataFrame(data)
    df.to_csv("wallet_fraud_dataset.csv", index=False)
    print("Success: 100,000 row dataset saved as 'wallet_fraud_dataset.csv'")

if __name__ == "__main__":
    generate_large_dataset(100000)
