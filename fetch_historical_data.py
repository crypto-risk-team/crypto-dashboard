from binance.client import Client
import pandas as pd
from datetime import datetime

client = Client()

symbols = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "SOLUSDT": "SOL",
    "ADAUSDT": "ADA",
    "DOGEUSDT": "DOGE"
}

all_data = []

for symbol, name in symbols.items():
    klines = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_1DAY,
        "1 year ago UTC"
    )

    for k in klines:
        all_data.append({
            "Date": datetime.fromtimestamp(k[0] / 1000),
            "Crypto": name,
            "Open": float(k[1]),
            "High": float(k[2]),
            "Low": float(k[3]),
            "Close": float(k[4]),
            "Volume": float(k[5])
        })

df = pd.DataFrame(all_data)
df.to_csv("data/historical_crypto_data.csv", index=False)

print("✅ Historical data saved successfully")
