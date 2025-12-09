import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# ---------------------------------------------------------
# Load OpenAI API Key from .env
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

st.title("AI-Powered Recognized Loss Calculator (OpenAI GPT-4.1)")

# ---------------------------------------------------------
# MASTER PROMPT FOR LOSS CALCULATION
# ---------------------------------------------------------
RULES_PROMPT = """
You are a financial loss-calculation engine.

Your job:
Given structured fund transactions, calculate TOTAL recognized loss per fund using STRICT rules:

RULES:
1. CLASS PERIOD = Feb 6, 2015 → Jul 28, 2015  
   Only purchases inside this window are eligible.

2. MATCHING METHOD = FIFO  
   Sales always match earliest available purchases.

3. DECLINE TABLE (Inflation Factors):
   A. Purchase ≤ Apr 28 2015:
        Sale ≤ Apr 28 2015 15:07 → 0
        Sale ≤ Aug 2 2015 → 12.93
        Sale ≥ Aug 3 2015 → 18.27

   B. Purchase Apr 29–Jul 28 2015:
        Sale ≤ Aug 2 2015 → 5.76
        Sale ≥ Aug 3 2015 → 7.41

   C. Purchase ≥ Jul 29 2015 → decline = 0

4. LOSS RULES:
   Sale ≤ Apr 28 2015 15:07 → Recognized Loss = 0  
   Sale ≤ Aug 2:
       loss = min(decline, purchase_price - sale_price)
   Sale ≥ Aug 3:
       loss = min(decline, purchase_price - sale_price, purchase_price - 28.06)

5. HELD SHARES as of Oct 30 2015:
       loss = min(decline, purchase_price - 28.06)

6. Negative values = 0.

FORMAT OF OUTPUT:
1. Present a clean table:
   Fund Name | Total Recognized Loss (USD)

2. Provide a short descriptive explanation:
   - How loss was computed  
   - Why any fund has 0 loss  
   - Any unusual patterns  

Be accurate, concise, and strict.
"""

# ---------------------------------------------------------
# SAFE NUMERIC CLEANING
# ---------------------------------------------------------
def safe_int(x):
    if pd.isna(x):
        return 0
    try:
        return int(float(str(x).replace(",", "").strip()))
    except:
        return 0


def safe_float(x):
    if pd.isna(x):
        return 0.0
    try:
        return float(str(x).replace(",", "").strip())
    except:
        return 0.0


# ---------------------------------------------------------
# CSV → CLEAN JSON FOR OPENAI
# ---------------------------------------------------------
def create_fund_payload(df):
    df = df.copy()
    df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    funds = {}
    for fund in df["Fund Name"].unique():
        subset = df[df["Fund Name"] == fund]
        funds[fund] = []

        for _, row in subset.iterrows():
            funds[fund].append({
                "type": str(row["Transaction Type"]).strip().lower(),
                "date": row["Trade Date"].strftime("%Y-%m-%d"),
                "price": safe_float(row["Price per share"]),
                "purchases": safe_int(row["Purchases"]),
                "sales": safe_int(row["Sales"])
            })

    return funds


# ---------------------------------------------------------
# SEND REQUEST TO OPENAI GPT-4.1
# ---------------------------------------------------------
def ask_openai(fund_json):
    prompt = f"""
{RULES_PROMPT}

Here is the structured transaction data:

{json.dumps(fund_json, indent=2)}

Now calculate total recognized loss per fund and provide explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenAI request failed: {e}"


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
uploaded = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.subheader("Uploaded CSV Data")
    st.dataframe(df)

    fund_payload = create_fund_payload(df)

    st.subheader("AI-Computed Recognized Loss")
    ai_output = ask_openai(fund_payload)

    st.markdown(ai_output)

else:
    st.info("Please upload a CSV to begin.")
