import pandas as pd

def load_data(path):
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def clean_data(df):
    df = df.drop_duplicates()

    df = df.dropna(
        subset=["sales", "quantity"]
    )

    df["sales"] = pd.to_numeric(
        df["sales"], errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"], errors="coerce"
        )

    df = df.dropna(subset=["sales"])

    return df


if __name__ == "__main__":
    df = load_data("../data/sales_data.csv")
    df = clean_data(df)

    print(df.head())
    print(df.info())
