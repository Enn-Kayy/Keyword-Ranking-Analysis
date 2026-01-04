import pandas as pd


def read_keywords(file_path: str):
    """
    Reads the input Excel file and extracts keyword–URL pairs
    in a normalized and validated format.
    """

    # Load Excel file
    df = pd.read_excel(file_path)

    # Standardize column names for reliable matching
    df.columns = df.columns.str.strip().str.lower()

    # Identify relevant columns dynamically
    column_map = {
        "keyword": None,
        "url": None
    }

    for col in df.columns:
        if col in ["keyword", "keywords"]:
            column_map["keyword"] = col
        elif col in ["url", "link", "page", "target_url"]:
            column_map["url"] = col

    # Validate required columns
    if not column_map["keyword"] or not column_map["url"]:
        raise ValueError(
            f"Excel columns found: {list(df.columns)}\n"
            f"Required columns: keyword, url"
        )

    # Rename detected columns to a consistent schema
    df = df.rename(columns={
        column_map["keyword"]: "keyword",
        column_map["url"]: "url"
    })

    # Remove rows with missing keyword or URL values
    df = df.dropna(subset=["keyword", "url"])

    # Return data in a record-oriented format for downstream processing
    return df.to_dict(orient="records")
