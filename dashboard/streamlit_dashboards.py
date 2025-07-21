import streamlit as st
import plotly.express as px
import pandas as pd

def dashboard_view(df):
    st.title("📊 BizBuddy Sales Dashboard")
    st.markdown("This dashboard shows key metrics and trends.")
    
    @st.cache_data
    def load_data():
        # Load Data from URL
        sheet_url = "https://docs.google.com/spreadsheets/d/1ISS7IQOMPrAEqU7lnpJYM5W2zd4oynntnmMTiokiVNU/export?format=csv"
        df = pd.read_csv(sheet_url)
        
        # Convert date column if found
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
        return df

    df = load_data()

    # Streamlit UI setup

    st.title("📊Dashboard")
    st.markdown("This dashboard shows key metrics and trends.")

    # KPI Cards
    total_revenue = df["Revenue"].sum()
    total_units = df["Units_Sold"].sum()
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

    # Revenue by Product
    st.subheader("📊 Revenue by Product")
    product_revenue = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    fig = px.bar(product_revenue, x=product_revenue.index, y="Revenue",
                    labels={"x": "Product", "y": "Revenue"}, title="Revenue by Product Category")
    st.plotly_chart(fig, use_container_width=True)

    # Revenue by Location
    st.subheader("📍 Revenue by Location")
    location_revenue = df.groupby("Location")["Revenue"].sum().sort_values(ascending=False)
    fig_location = px.bar(location_revenue, x=location_revenue.index, y="Revenue",
                            labels={"x": "Location", "y": "Revenue"}, title="Revenue by Location")
    st.plotly_chart(fig_location, use_container_width=True)

    # Revenue by Platform
    st.subheader("💻 Revenue by Platform") 
    platform_revenue = df.groupby("Platform")["Revenue"].sum().sort_values(ascending=False)
    fig_platform = px.bar(platform_revenue, x=platform_revenue.index, y="Revenue",
                            labels={"x": "Platform", "y": "Revenue"}, title="Revenue by Platform")
    st.plotly_chart(fig_platform, use_container_width=True)

    # Inventory Status
    st.subheader("📦 Inventory Status")
    inventory_status = df.groupby("Product")["Inventory_After"].sum().sort_values(ascending=False)
    fig_inventory = px.bar(inventory_status, x=inventory_status.index, y="Inventory_After",
                            labels={"x": "Product", "y": "Inventory After"}, title="Inventory Status by Product")
    st.plotly_chart(fig_inventory, use_container_width=True)    

    #Product with low inventory
    st.subheader("⚠️ Products with Low Inventory")
    low_inventory = df[df["Inventory_After"] < 10]
    if not low_inventory.empty:
        low_inventory = low_inventory.groupby("Product")["Inventory_After"].min().sort_values().reset_index().head(10)
        st.table(low_inventory)
    else:
        st.write("No products with low inventory.")
