import random
from datetime import datetime

symbols = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK"
]

def generate_tick():
    return {
        "symbol": random.choice(symbols),
        "price": round(random.uniform(500, 3000), 2),
        "volume": random.randint(100, 10000),
        "timestamp": datetime.now().isoformat()
    }