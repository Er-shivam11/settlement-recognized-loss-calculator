import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Fund Transactions Table with Strict Recognized Loss Calculation")

# Helper: parse date
def parse_date(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y")

# Simplified Table 1 (decline in inflation) per rule
def get_inflation_decline(purchase_date, sale_date):
    # Sale before Aug 3, 2015
    if purchase_date <= datetime(2015, 4, 28):
        if sale_date <= datetime(2015, 4, 28, 15, 7):
            return 0.0
        elif sale_date <= datetime(2015, 8, 2):
            return 12.93
        else:
            return 18.27
    elif datetime(2015, 4, 29) <= purchase_date <= datetime(2015, 7, 28):
        if sale_date <= datetime(2015, 8, 2):
            return 5.76
        else:
            return 7.41
    elif purchase_date >= datetime(2015, 7, 29):
        return 0.0
    return 0.0

# Average closing price for held shares (Table 2)
avg_closing_price = 28.06

# Main function: calculate recognized loss per fund
def calculate_recognized_loss(df):
    loss_summary = {}

    # Clean numeric columns
    numeric_cols = ['Purchases', 'Sales', 'Holdings', 'Price per share']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].replace({',': ''}, regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Filter only purchases during Class Period
    class_period_start = datetime(2015, 2, 6)
    class_period_end = datetime(2015, 7, 28)

    funds = df['Fund Name'].unique()
    for fund in funds:
        fund_df = df[df['Fund Name'] == fund].copy()
        purchases = []

        total_loss = 0.0

        for idx, row in fund_df.iterrows():
            trade_type = row['Transaction Type'].strip().lower()
            trade_date = parse_date(row['Trade Date'])
            price = row['Price per share']
            shares = row['Purchases']

            # Only consider purchases during Class Period
            if trade_type == 'purchase' and class_period_start <= trade_date <= class_period_end and shares > 0:
                purchases.append({'shares': shares, 'price': price, 'date': trade_date})
            elif trade_type == 'sale' and row['Sales'] > 0:
                sale_shares = row['Sales']
                sale_price = price

                # Match sale against purchases FIFO
                i = 0
                while sale_shares > 0 and i < len(purchases):
                    p = purchases[i]
                    if p['shares'] <= 0:
                        i += 1
                        continue

                    matched_shares = min(p['shares'], sale_shares)

                    # Apply strict rules
                    if trade_date <= datetime(2015, 4, 28, 15, 7):
                        recognized_loss = 0
                    elif trade_date <= datetime(2015, 8, 2):
                        decline = get_inflation_decline(p['date'], trade_date)
                        recognized_loss = min(decline, p['price'] - sale_price)
                        recognized_loss = max(recognized_loss, 0)
                    else:
                        decline = get_inflation_decline(p['date'], trade_date)
                        recognized_loss = min(decline, p['price'] - sale_price, p['price'] - avg_closing_price)
                        recognized_loss = max(recognized_loss, 0)

                    total_loss += recognized_loss * matched_shares

                    # Update remaining shares
                    p['shares'] -= matched_shares
                    sale_shares -= matched_shares
                    if p['shares'] <= 0:
                        i += 1

        # Handle remaining held shares as of 10/30/2015
        for p in purchases:
            if p['shares'] > 0:
                decline = get_inflation_decline(p['date'], datetime(2015, 10, 30))
                recognized_loss = min(decline, p['price'] - avg_closing_price)
                recognized_loss = max(recognized_loss, 0)
                total_loss += recognized_loss * p['shares']

        loss_summary[fund] = total_loss

    return pd.DataFrame(list(loss_summary.items()), columns=['Fund Name', 'Total Recognized Loss (USD)'])

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Fund Transactions Data")
    st.dataframe(df)

    # Calculate recognized loss
    fund_loss_summary = calculate_recognized_loss(df)

    st.subheader("Final Recognized Loss per Fund")
    st.dataframe(fund_loss_summary)

else:
    st.info("Please upload a CSV file to see the table.")
