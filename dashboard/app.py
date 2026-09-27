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

    # Load dataset
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Unable to read CSV file: {e}")
        st.stop()

    # --------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Remove duplicate columns if any
    df = df.loc[:, ~df.columns.duplicated()]

    # --------------------------------------------------
    # AUTOMATIC COLUMN DETECTION
    # --------------------------------------------------

    def find_column(candidates):
        for column in candidates:
            if column in df.columns:
                return column
        return None

    sales_col = find_column([
        "sales",
        "total_sales",
        "sales_amount",
        "revenue",
        "total_revenue"
    ])

    quantity_col = find_column([
        "quantity",
        "qty",
        "units",
        "units_sold"
    ])

    order_col = find_column([
        "order_id",
        "orderid",
        "order_number",
        "order"
    ])

    category_col = find_column([
        "category",
        "product_category",
        "product_category_name"
    ])

    region_col = find_column([
        "region",
        "sales_region",
        "area",
        "territory"
    ])

    # --------------------------------------------------
    # VALIDATE REQUIRED SALES COLUMN
    # --------------------------------------------------

    if sales_col is None:

        st.error("❌ Sales/Revenue column not found.")

        st.info(
            "Please make sure your dataset contains a sales "
            "or revenue column."
        )

        st.write("### Columns detected in your dataset:")
        st.write(list(df.columns))

        st.stop()

    # Convert sales to numeric
    df[sales_col] = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------
    # QUANTITY
    # --------------------------------------------------

    if quantity_col:

        df[quantity_col] = pd.to_numeric(
            df[quantity_col],
            errors="coerce"
        ).fillna(0)

        total_quantity = df[quantity_col].sum()

    else:

        total_quantity = 0

    # --------------------------------------------------
    # KPIs
    # --------------------------------------------------

    total_sales = df[sales_col].sum()

    if order_col:
        total_orders = df[order_col].nunique()
    else:
        total_orders = len(df)

    avg_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

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
        f"{total_quantity:,.0f}"
    )

    col4.metric(
        "Avg Order Value",
        f"₹{avg_order_value:,.0f}"
    )

    st.divider()

    # --------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------

    if category_col:

        category_sales = (
            df.groupby(category_col)[sales_col]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_sales,
            x=category_col,
            y=sales_col,
            title="Sales by Category",
            labels={
                category_col: "Category",
                sales_col: "Sales"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------
    # REGION ANALYSIS
    # --------------------------------------------------

    if region_col:

        region_sales = (
            df.groupby(region_col)[sales_col]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            region_sales,
            names=region_col,
            values=sales_col,
            title="Sales Distribution by Region"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Dataset Overview")

    info1, info2, info3 = st.columns(3)

    info1.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

    info2.metric(
        "Columns",
        f"{df.shape[1]:,}"
    )

    info3.metric(
        "Missing Values",
        f"{df.isna().sum().sum():,}"
    )

    # --------------------------------------------------
    # RAW DATA
    # --------------------------------------------------

    with st.expander("🔍 View Dataset"):

        st.dataframe(
            df,
            use_container_width=True
        )
