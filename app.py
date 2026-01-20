from flask import Flask, render_template, redirect
import requests
import pandas as pd


app = Flask(__name__)
def fetch_live_crypto_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"

    symbols = {
        "BTCUSDT": "Bitcoin",
        "ETHUSDT": "Ethereum",
        "SOLUSDT": "Solana",
        "ADAUSDT": "Cardano",
        "DOGEUSDT": "Dogecoin"
    }

    response = requests.get(url).json()
    data = []

    for item in response:
        if item["symbol"] in symbols:
            data.append({
                "name": symbols[item["symbol"]],
                "price": round(float(item["lastPrice"]), 4),
                "change": round(float(item["priceChangePercent"]), 2),
                "volume": int(float(item["volume"]))
            })

    return data
@app.route("/")
def index():
    return redirect("/home")
@app.route("/home")
def home():
    return render_template("home.html")

# ---------------- HOME ----------------
@app.route("/milestone1")
def milestone1():

    cryptos = fetch_live_crypto_data()

    days = [f"Day {i+1}" for i in range(7)]

    price_trends = {
        "Bitcoin": [86000, 86500, 87000, 87500, 87800, 87950, 88002],
        "Ethereum": [2800, 2820, 2850, 2900, 2920, 2940, 2950],
        "Solana": [115, 118, 120, 122, 123, 124, 124.6],
        "Cardano": [0.55, 0.56, 0.57, 0.58, 0.58, 0.59, 0.58],
        "Dogecoin": [0.075, 0.077, 0.078, 0.080, 0.081, 0.082, 0.082]
    }

    return render_template(
        "milestone1.html",
        cryptos=cryptos,
        days=days,
        price_trends=price_trends
    )

# ---------------- MILESTONE 2 ----------------
@app.route("/milestone2")
def milestone2():
    from flask import request
    import pandas as pd
    import numpy as np

    # Get selected days (default = 30)
    days = int(request.args.get("days", 30))

    # ----- DUMMY HISTORICAL RETURNS (exam-safe) -----
    np.random.seed(42)

    cryptos = ["BTC", "ETH", "SOL", "ADA", "DOGE"]
    data = {}

    for c in cryptos:
        data[c] = np.random.normal(0.001, 0.02, days)

    returns_df = pd.DataFrame(data)

    # ----- METRICS CALCULATION -----
    volatility = returns_df.std() * np.sqrt(252)
    sharpe = returns_df.mean() / returns_df.std()
    beta = {
        "BTC": 1.0,
        "ETH": 1.15,
        "SOL": 1.87,
        "ADA": 1.42,
        "DOGE": 2.13
    }

    metrics = pd.DataFrame({
        "Crypto": cryptos,
        "Volatility": volatility.values.round(3),
        "Sharpe": sharpe.values.round(3),
        "Beta": [beta[c] for c in cryptos]
    })

    labels = metrics["Crypto"].tolist()
    volatility_values = metrics["Volatility"].tolist()

    return render_template(
        "milestone2.html",
        metrics=metrics,
        labels=labels,
        volatility_values=volatility_values,
        selected_days=days
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


