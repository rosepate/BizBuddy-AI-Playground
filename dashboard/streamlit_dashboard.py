import streamlit as st
import plotly.express as px
import pandas as pd
import pdfkit
import tempfile

# Dashboard view function
@st.cache_data
def load_data():
    #Load Data from URL
    sheet_url = "https://docs.google.com/spreadsheets/d/1wKl1K0d0M_S_GUnOfw-duIhBc59YSU8KBKwWsPO26jI/export?format=csv"
    df = pd.read_csv(sheet_url)
    
    df.columns = df.columns.str.strip()
    df.rename(columns={"Order Date": "Date"}, inplace=True)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    if "Expiry Date" in df.columns:
        df["Expiry Date"] = pd.to_datetime(df["Expiry Date"], errors='coerce')

    # Handle missing values
    df.fillna(0, inplace=True)
    # Ensure all required columns are present
    required_cols = ["Units Sold", "Revenue", "Cost Price", "Unit Price", "Profit", "Product", "Location", "Inventory After", "Date"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # Print columns and sample data for debugging
    print("🧾 Columns in dataset:", df.columns.tolist())
    print("🔍 Sample data:\n", df.head())

    return df
df = load_data()

# Streamlit UI setup
st.title("Dashboard")
st.markdown("This dashboard shows key metrics and trends.")

# KPI Cards
total_revenue = df["Revenue"].sum()
total_units = df["Units Sold"].sum()
top_product = df.groupby("Product")["Revenue"].sum().idxmax()
top_location = df.groupby("Location")["Revenue"].sum().idxmax()
col1, col2, col3, col4 = st.columns(4)
col1.metric("💵 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Units Sold", f"{total_units:,}")
col3.metric("🏆 Top Product", top_product)
col4.metric("📍 Top Location", top_location)

# Revenue over time
st.subheader("📈 Monthly Revenue Trend")
monthly = df.groupby(pd.Grouper(key='Date', freq='M'))["Revenue"].sum().reset_index()
st.line_chart(monthly.rename(columns={"Date": "Month"}).set_index("Month")) 
# Revenue by Category
st.subheader("📊 Revenue by Product Category")
print(df.columns.tolist())
df.columns = df.columns.str.strip()
product_revenue = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
print("product Revenue:", product_revenue)
st.bar_chart(product_revenue)
category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
st.bar_chart(category_revenue)
#Revenue by Platform
st.subheader("🛍️ Revenue by Platform")
platform_revenue = df.groupby("Platform")["Revenue"].sum().sort_values(ascending=False)
st.bar_chart(platform_revenue)
# Revenue by Location
st.subheader("🗺️ Revenue by Location")
location_revenue = df.groupby("Location")["Revenue"].sum().reset_index()
fig = px.bar(location_revenue, x="Location", y="Revenue", color="Location", title="Revenue by Location")
st.plotly_chart(fig)    
# Low Inventory Alerts
st.subheader("📦 Products with Low Inventory")
low_stock = df[df["Inventory After"] < 20].groupby("Product")["Inventory After"].min().sort_values().reset_index().head(10)
st.dataframe(low_stock)
# Upcoming Expiry Medicines
st.subheader("⏰ Upcoming Expiry Medicines (Next 60 Days)")
exp_soon = df[df["Expiry Date"] <= pd.Timestamp.today() + pd.Timedelta(days=60)]
st.dataframe(exp_soon[["Product", "Expiry Date", "Inventory After"]].drop_duplicates()) 
# Download button
st.download_button("📥 Download Full Data as CSV", df.to_csv(index=False), "pharmacy_data.csv", "text/csv") 
