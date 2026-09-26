import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide"
)

st.title("📊 Sales Performance Analysis")

uploaded_file = st.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Cleaning
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # KPIs
    total_sales = df["sales"].sum()
    total_quantity = df["quantity"].sum()

    total_orders = (
        df["order_id"].nunique()
        if "order_id" in df.columns
        else len(df)
    )

    avg_order_value = (
        total_sales / total_orders
        if total_orders else 0
    )

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sales",
        f"₹{total_sales:,.0f}"
    )

    col2.metric(
        "Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Quantity Sold",
        f"{total_quantity:,}"
    )

    col4.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

    st.divider()

    # Category analysis
    if "category" in df.columns:

        category_sales = (
            df.groupby("category")["sales"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x="category",
            y="sales",
            title="Sales by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Region analysis
    if "region" in df.columns:

        region_sales = (
            df.groupby("region")["sales"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            region_sales,
            names="region",
            values="sales",
            title="Sales Distribution by Region"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Raw data
    with st.expander("View Dataset"):
        st.dataframe(
            df,
            use_container_width=True
        )
