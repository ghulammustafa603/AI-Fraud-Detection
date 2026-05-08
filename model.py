import random
from datetime import datetime

# ==========================================
# RISK WEIGHTING CONFIGURATION
# ==========================================
# These weights are inspired by fintech security standards for mobile wallets.
WEIGHTS = {
    "TIMING": 0.25,        # Midnight to Dawn (High risk period)
    "AMOUNT_SPIKE": 0.20,  # Deviation from historical average
    "NEW_DEVICE": 0.20,    # Unrecognized hardware signature
    "LOCATION": 0.15,      # City-level mismatch
    "FREQUENCY": 0.12,     # Multiple transactions in a short window
    "DEMOGRAPHICS": 0.08   # Age/Gender vulnerability profiles
}

CITIES = ["Karachi", "Lahore", "Faisalabad", "Peshawar", "Quetta", "Multan"]
WALLETS = ["JazzCash", "Easypaisa"]

def calculate_risk(tx):
    """
    Core Risk Scoring Engine.
    Calculates a score from 0-100 based on 6 security dimensions.
    """
    # 1. Timing (25%): 12 AM - 6 AM
    hour = tx['time'].hour
    timing_risk = 100 if (0 <= hour <= 6) else 0
    
    # 2. Amount Spike (20%): > 3x historical (Base: Rs. 5000)
    hist_avg = 5000
    amount_risk = 100 if (tx['amount'] > 3 * hist_avg) else (min(100, (tx['amount']/hist_avg)*30))
    
    # 3. New Device (20%)
    device_risk = 100 if tx['is_new_device'] else 0
    
    # 4. Location Change (15%)
    location_risk = 100 if tx['is_loc_mismatch'] else 0
    
    # 5. Frequency (12%)
    freq_risk = 100 if tx['high_freq'] else 0
    
    # 6. Demographics (8%)
    demo_risk = 100 if (tx['user_age'] > 60 or tx['user_age'] < 18) else 0
    
    # Weighted Sum Formula
    final_score = (
        (timing_risk * WEIGHTS["TIMING"]) + 
        (amount_risk * WEIGHTS["AMOUNT_SPIKE"]) + 
        (device_risk * WEIGHTS["NEW_DEVICE"]) + 
        (location_risk * WEIGHTS["LOCATION"]) + 
        (freq_risk * WEIGHTS["FREQUENCY"]) + 
        (demo_risk * WEIGHTS["DEMOGRAPHICS"])
    )
    
    return round(final_score, 1), {
        "Timing": timing_risk,
        "Amount": amount_risk,
        "Device": device_risk,
        "Location": location_risk,
        "Frequency": freq_risk,
        "Demographics": demo_risk
    }

def generate_transaction():
    """Generates synthetic Pakistani wallet transaction data."""
    is_fraud_scenario = random.random() < 0.15 
    
    if is_fraud_scenario:
        amount = random.randint(25000, 100000)
        hour = random.choice([1, 2, 3, 4, 5])
        is_new_device = random.choice([True, False, True])
        is_loc_mismatch = random.choice([True, False, True])
        high_freq = random.choice([True, False])
        age = random.choice([16, 72, 25, 30])
    else:
        amount = random.randint(100, 15000)
        hour = random.randint(7, 23)
        is_new_device = False
        is_loc_mismatch = False
        high_freq = False
        age = random.randint(20, 50)

    now = datetime.now()
    tx_time = now.replace(hour=hour, minute=random.randint(0, 59))
    
    return {
        "id": f"TXN-{random.randint(10000, 99999)}",
        "wallet": random.choice(WALLETS),
        "city": random.choice(CITIES),
        "amount": amount,
        "time": tx_time,
        "is_new_device": is_new_device,
        "is_loc_mismatch": is_loc_mismatch,
        "high_freq": high_freq,
        "user_age": age,
        "user_gender": random.choice(["Male", "Female"])
    }
