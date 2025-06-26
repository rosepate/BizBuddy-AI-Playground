import streamlit as st
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv

st.set_page_config(page_title="📊 BizBuddy Sales Dashboard", page_icon="📈", layout="wide")

# Load environment variables
load_dotenv()

# Load data
import os

base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "..", "Supplement_Sales_Weekly_Expanded.csv")
df = pd.read_csv(csv_path)

@st.cache_data
def load_data():
    df = pd.read_csv("Supplement_Sales_Weekly_Expanded.csv")
    # Convert date column if found
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
    return df

df = load_data()

# Streamlit UI setup

st.title("📊 Supplement Sales Dashboard")
st.markdown("This dashboard shows key metrics and trends in supplement sales from 2020–2023.")

# KPI Cards
total_revenue = df["Revenue"].sum()
total_units = df["Units Sold"].sum()
top_product = df.groupby("Product Name")["Revenue"].sum().idxmax()
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
category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
st.bar_chart(category_revenue)

# Revenue by Platform
st.subheader("🛍️ Revenue by Platform")
platform_revenue = df.groupby("Platform")["Revenue"].sum().sort_values(ascending=False)
st.bar_chart(platform_revenue)

#Unit sold over time
st.subheader("📦 Units Sold Over Time")
monthly_units = df.groupby(pd.Grouper(key="Date", freq="M"))["Units Sold"].sum().reset_index()
st.line_chart(monthly_units.rename(columns={"Date": "Month"}).set_index("Month"))

#  Revenue Share by Category 

st.subheader("📂 Revenue Share by Product Category")
category_revenue = df.groupby("Category")["Revenue"].sum().reset_index()
fig = px.pie(category_revenue, values="Revenue", names="Category", title="Revenue Share by Category")
st.plotly_chart(fig)

#Location-Wise Revenue and Returns
st.subheader("📍 Revenue vs Returns by Location")
location_summary = df.groupby("Location")[["Revenue", "Units Returned"]].sum().reset_index()
fig = px.bar(location_summary, x="Location", y=["Revenue", "Units Returned"], barmode="group")
st.plotly_chart(fig)

# Discount vs Units Sold
st.subheader("🔄 Discount vs Units Sold")
fig = px.scatter(df, x="Discount", y="Units Sold", color="Category", size="Revenue",
                 title="Impact of Discount on Units Sold")
st.plotly_chart(fig)

# Top 10 Products with Most Returns
st.subheader("🚨 Top 10 Products with Most Returns")
returns_by_product = (
    df.groupby("Product Name")["Units Returned"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_returns = px.bar(
    returns_by_product,
    x="Units Returned",
    y="Product Name",
    orientation="h",
    title="Top 10 Products with Most Units Returned",
    labels={"Product Name": "Product"},
)
st.plotly_chart(fig_returns)

# Month-over-Month Revenue Growth

st.subheader("📈 Month-over-Month Revenue Growth")
monthly_revenue = df.groupby(pd.Grouper(key="Date", freq="M"))["Revenue"].sum().reset_index()
monthly_revenue["MoM Growth (%)"] = monthly_revenue["Revenue"].pct_change() * 100

fig_growth = px.line(
    monthly_revenue,
    x="Date",
    y="MoM Growth (%)",
    title="Month-over-Month Revenue Growth (%)",
    markers=True,
)
st.plotly_chart(fig_growth)


# Filtered Sales Explorer
st.subheader("🔍 Explore Filtered Sales Data")
with st.expander("📍 Filter Options"):
    category = st.selectbox("Choose Category", ["All"] + sorted(df["Category"].unique()))
    location = st.selectbox("Choose Location", ["All"] + sorted(df["Location"].unique()))

filtered_df = df.copy()
if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]
if location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location]

st.dataframe(filtered_df)