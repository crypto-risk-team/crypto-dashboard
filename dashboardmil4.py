import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Risk Classification", layout="wide")

st.title("📊 Milestone 4: Risk Classification & Reporting")

# ------------------------------
# LOAD FINAL PROCESSED DATA
# ------------------------------
df = pd.read_csv("data/historical_crypto_data.csv", parse_dates=["Date"])

# Calculate returns & volatility
df["Return"] = df.groupby("Crypto")["Close"].pct_change()

summary = df.groupby("Crypto").agg(
    Volatility=("Return", "std"),
    Avg_Return=("Return", "mean")
).dropna().reset_index()

summary["Volatility"] = summary["Volatility"] * 100  # percentage

# ------------------------------
# DATA-DRIVEN RISK CLASSIFICATION
# ------------------------------
low_threshold = summary["Volatility"].quantile(0.33)
high_threshold = summary["Volatility"].quantile(0.66)

def classify_risk(vol):
    if vol <= low_threshold:
        return "Low Risk"
    elif vol <= high_threshold:
        return "Medium Risk"
    else:
        return "High Risk"

summary["Risk Level"] = summary["Volatility"].apply(classify_risk)


# ------------------------------
# DASHBOARD LAYOUT
# ------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔴 High Risk")
    high = summary[summary["Risk Level"] == "High Risk"]
    for _, r in high.iterrows():
        st.error(f"{r['Crypto']} — {r['Volatility']:.2f}%")

with col2:
    st.subheader("🟡 Medium Risk")
    mid = summary[summary["Risk Level"] == "Medium Risk"]
    for _, r in mid.iterrows():
        st.warning(f"{r['Crypto']} — {r['Volatility']:.2f}%")

with col3:
    st.subheader("🟢 Low Risk")
    low = summary[summary["Risk Level"] == "Low Risk"]
    for _, r in low.iterrows():
        st.success(f"{r['Crypto']} — {r['Volatility']:.2f}%")

# ------------------------------
# RISK DISTRIBUTION CHART
# ------------------------------
st.subheader("📊 Risk Distribution")

dist = summary["Risk Level"].value_counts().reset_index()
dist.columns = ["Risk Level", "Count"]

fig = px.pie(
    dist,
    names="Risk Level",
    values="Count",
    color="Risk Level",
    color_discrete_map={
        "High Risk": "red",
        "Medium Risk": "orange",
        "Low Risk": "green"
    }
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# SUMMARY REPORT
# ------------------------------
st.subheader("📄 Risk Summary Report")

st.write(f"**Total Cryptocurrencies:** {len(summary)}")
st.write(f"**Average Volatility:** {summary['Volatility'].mean():.2f}%")
st.write(
    f"**Risk Distribution:** "
    f"{len(high)} High / {len(mid)} Medium / {len(low)} Low"
)

# ------------------------------
# EXPORT OPTIONS
# ------------------------------
st.download_button(
    "⬇ Download CSV Report",
    summary.to_csv(index=False),
    file_name="crypto_risk_report.csv",
    mime="text/csv"
)

st.success("✅ Milestone 4 Completed Successfully")
