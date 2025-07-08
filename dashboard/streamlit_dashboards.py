import streamlit as st
import plotly.express as px
import pandas as pd
import pdfkit
import tempfile


def dashboard_view(df):
    st.title("📊 Supplement Sales Dashboard")
    st.markdown("This dashboard shows key metrics and trends in supplement sales from 2020–2023.")

    # KPI Cards
    total_revenue = df["Revenue"].sum()
    total_units = df["Units Sold"].sum()
    top_product = df.groupby("Product Name")["Revenue"].sum().idxmax()
    top_location = df.groupby("Location")["Revenue"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📦 Units Sold", f"{total_units:,}")
    col3.metric("🏆 Top Product", top_product)
    col4.metric("📍 Top Location", top_location)

    st.subheader("📈 Monthly Revenue Trend")
    monthly = df.groupby(pd.Grouper(key='Date', freq='M'))["Revenue"].sum().reset_index()
    st.line_chart(monthly.set_index("Date"))

    st.subheader("📊 Revenue by Product Category")
    category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    st.bar_chart(category_revenue)

    st.subheader("🛍️ Revenue by Platform")
    platform_revenue = df.groupby("Platform")["Revenue"].sum().sort_values(ascending=False)
    st.bar_chart(platform_revenue)

    st.subheader("📦 Units Sold Over Time")
    monthly_units = df.groupby(pd.Grouper(key="Date", freq="M"))["Units Sold"].sum().reset_index()
    st.line_chart(monthly_units.set_index("Date"))

    st.subheader("📂 Revenue Share by Category")
    pie_data = df.groupby("Category")["Revenue"].sum().reset_index()
    fig = px.pie(pie_data, values="Revenue", names="Category")
    st.plotly_chart(fig)

    st.subheader("📍 Revenue vs Returns by Location")
    loc_summary = df.groupby("Location")[["Revenue", "Units Returned"]].sum().reset_index()
    fig2 = px.bar(loc_summary, x="Location", y=["Revenue", "Units Returned"], barmode="group")
    st.plotly_chart(fig2)

    st.subheader("🔄 Discount vs Units Sold")
    fig3 = px.scatter(df, x="Discount", y="Units Sold", color="Category", size="Revenue")
    st.plotly_chart(fig3)

    st.subheader("🚨 Top 10 Products with Most Returns")
    returns = df.groupby("Product Name")["Units Returned"].sum().sort_values(ascending=False).head(10).reset_index()
    fig4 = px.bar(returns, x="Units Returned", y="Product Name", orientation="h")
    st.plotly_chart(fig4)

    st.subheader("📈 Month-over-Month Revenue Growth (%)")
    monthly["MoM Growth (%)"] = monthly["Revenue"].pct_change() * 100
    fig5 = px.line(monthly, x="Date", y="MoM Growth (%)", markers=True)
    st.plotly_chart(fig5)

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

    # 📄 Full dashboard print-to-PDF button
    with st.expander("📄 Export Dashboard as PDF"):
        st.markdown("""
            <style>
            .print-button {
                background-color: #2b7de9;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
            }
            </style>

            <center>
            <button class="print-button" onclick="window.print()">📄 Download Full Dashboard as PDF</button>
            </center>
        """, unsafe_allow_html=True)

        st.markdown("""
            **How it works:**
            - Click the button above
            - When your browser's print window opens, choose **Destination: Save as PDF**
            - Click **Save**
        """)
