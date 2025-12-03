import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def clean_column_names(df):
    # Standardize column names to lowercase remove whitespace and replace spaces with underscores
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

    # remove double spaces in prodname and category columns
    if 'prodname' in df.columns:
        df['prodname'] = df['prodname'].str.replace('  ', ' ').str.lower().str.strip()
    if 'category' in df.columns:
        df['category'] = df['category'].str.replace('  ', ' ').str.lower().str.strip()

    return df


def handle_missing_values(df):
    # fill spaces or double spaces in price and qty columns with a zero
    df['price'] = df['price'].replace(' ', 0).replace('  ', 0).astype(float)
    df['qty'] = df['qty'].replace(' ', 0).replace('  ', 0).astype(int)

    # Strip leading and trailing whitespace from all the data under prodname and category columns remove the quotation marks if any
    df['prodname'] = df['prodname'].str.strip().str.replace('"', '')
    df['category'] = df['category'].str.replace('"', '').str.strip()
    df['category'] = df['category'].str.strip()

    # Handle missing values by filling them with appropriate defaults for columns prodname, price, qty, and date_sold
    df['prodname'] = df['prodname'].fillna('Unknown Product')
    df['price'] = df['price'].fillna(0)
    df['qty'] = df['qty'].fillna(0)
    df['date_sold'] = pd.to_datetime(df['date_sold'], errors='coerce')
    df['date_sold'] = df['date_sold'].fillna(pd.Timestamp('2024-01-01'))

    # remove negative values in price and qty columns by converting them to absolute values
    df['price'] = df['price'].abs()
    df['qty'] = df['qty'].abs()

    return df

def remove_invalid_rows(df):
    # Remove duplicates
    df = df.drop_duplicates()
    return df

# Show the new cleaned DataFrame
print("-" * 100)

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())