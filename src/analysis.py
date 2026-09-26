import pandas as pd


def calculate_kpis(df):

    total_sales = df["sales"].sum()

    total_orders = (
        df["order_id"].nunique()
        if "order_id" in df.columns
        else len(df)
    )

    total_quantity = df["quantity"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0 else 0
    )

    return {
        "Total Sales": total_sales,
        "Total Orders": total_orders,
        "Total Quantity": total_quantity,
        "Average Order Value": average_order_value
    }


def sales_by_category(df):
    return (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )


def sales_by_region(df):
    return (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )


def sales_by_product(df):
    return (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
    )


def monthly_sales(df):

    df["month"] = df["date"].dt.to_period("M")

    return (
        df.groupby("month")["sales"]
        .sum()
        .reset_index()
    )
