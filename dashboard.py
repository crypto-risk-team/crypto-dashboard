import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Crypto Risk Dashboard", layout="wide")

st.title("📊 Crypto Risk Analytics Dashboard")

# ------------------------------
# LOAD HISTORICAL DATA
# ------------------------------
df = pd.read_csv("data/historical_crypto_data.csv", parse_dates=["Date"])

# ------------------------------
# SIDEBAR CONTROLS
# ------------------------------
st.sidebar.header("Controls")

cryptos = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    df["Crypto"].unique(),
    default=df["Crypto"].unique()
)

days = st.sidebar.selectbox("Select Time Range", [30, 90, 365])

filtered_df = df[df["Crypto"].isin(cryptos)]
filtered_df = filtered_df.groupby("Crypto").tail(days)

# ------------------------------
# RETURNS & VOLATILITY
# ------------------------------
filtered_df["Return"] = filtered_df.groupby("Crypto")["Close"].pct_change()

filtered_df["Volatility"] = (
    filtered_df.groupby("Crypto")["Return"]
    .rolling(7)
    .std()
    .reset_index(level=0, drop=True)
)

# ------------------------------
# PRICE TREND
# ------------------------------
st.subheader("📈 Price Trend")

price_fig = px.line(
    filtered_df,
    x="Date",
    y="Close",
    color="Crypto"
)
st.plotly_chart(price_fig, use_container_width=True)

# ------------------------------
# VOLATILITY TREND
# ------------------------------
st.subheader("📊 Volatility Trend")

vol_fig = px.line(
    filtered_df,
    x="Date",
    y="Volatility",
    color="Crypto"
)
st.plotly_chart(vol_fig, use_container_width=True)

# ------------------------------
# RISK–RETURN SCATTER
# ------------------------------
st.subheader("⚖ Risk–Return Analysis")

summary = filtered_df.groupby("Crypto").agg(
    Avg_Return=("Return", "mean"),
    Volatility=("Return", "std")
).dropna().reset_index()

scatter = px.scatter(
    summary,
    x="Volatility",
    y="Avg_Return",
    color="Crypto",
    size="Volatility",
    title="Risk vs Return"
)

st.plotly_chart(scatter, use_container_width=True)

# ------------------------------
# METRIC CARDS
# ------------------------------
st.subheader("📌 Risk Metrics")

for _, row in summary.iterrows():
    st.write(
        f"**{row['Crypto']}** | Volatility: {row['Volatility']:.4f} | "
        f"Avg Return: {row['Avg_Return']:.4f}"
    )
