import matplotlib.pyplot as plt
import seaborn as sns


def plot_sales_by_category(df):

    data = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))

    sns.barplot(
        x=data.values,
        y=data.index
    )

    plt.title("Sales by Category")
    plt.xlabel("Sales")
    plt.ylabel("Category")
    plt.tight_layout()

    plt.show()


def plot_monthly_sales(df):

    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby("month")["sales"]
        .sum()
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        monthly.index.astype(str),
        monthly.values,
        marker="o"
    )

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
