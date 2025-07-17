import pandas as pd

def get_csv_download_link(df: pd.DataFrame, filename="filtered_flights.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    return csv, filename
