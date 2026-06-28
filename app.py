import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ──────────────────────────────────────────
# EXTRACT
# ──────────────────────────────────────────
def extract():
    print("[1/3] Extracting data...")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    df = pd.read_csv(url)
    print(df.columns.tolist())
    print(f"    Raw rows fetched: {len(df)}")
    return df

# ──────────────────────────────────────────
# TRANSFORM
# ──────────────────────────────────────────
def transform(df):
    print("[2/3] Transforming data...")

    # Select only the columns we care about
    cols = [
        'iso_code', 'location', 
        'total_cases', 'new_cases',
        'total_deaths', 'new_deaths',
        'total_vaccinations', 'population'
    ]
    df = df[cols].copy()

    # Drop aggregated regions (World, Asia, Europe, etc.)
    df = df[~df['iso_code'].str.startswith('OWID', na=False)]

    # Drop rows missing critical fields
    df = df.dropna(subset=['location', 'total_cases'])

    # Fill remaining nulls with 0
    df = df.fillna(0)

    # Add a pipeline run timestamp
    df['loaded_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # DATA QUALITY CHECK
    null_count = df['total_cases'].isnull().sum()
    row_count = len(df)
    print(f"    Rows after cleaning: {row_count}")
    print(f"    Null total_cases: {null_count}  ({'PASS' if null_count == 0 else 'FAIL'})")

    return df

# ──────────────────────────────────────────
# LOAD
# ──────────────────────────────────────────
def load(df):
    print("[3/3] Loading into SQLite...")

    conn = sqlite3.connect("covid_data.db")  # creates the file if it doesn't exist
    df.to_sql("covid_summary", conn, if_exists="replace", index=False)

    # Verify load
    row_count = pd.read_sql("SELECT COUNT(*) as cnt FROM covid_summary", conn).iloc[0]['cnt']
    print(f"    Rows loaded into DB: {row_count}")
    conn.close()
    print("    Saved to: covid_data.db")

# ──────────────────────────────────────────
# QUERY & VISUALIZE
# ──────────────────────────────────────────
def report():
    conn = sqlite3.connect("covid_data.db")

    # Top 10 countries by total cases
    query = """
        SELECT location, total_cases, total_deaths, new_cases
        FROM covid_summary
        ORDER BY total_cases DESC
        LIMIT 10
    """
    top10 = pd.read_sql(query, conn)
    conn.close()

    print("\nTop 10 Countries by Total Cases:")
    print(top10.to_string(index=False))

    # Bar chart
    plt.figure(figsize=(12, 5))
    plt.bar(top10['location'], top10['total_cases'] / 1e6, color='steelblue')
    plt.title("Top 10 Countries — Total COVID-19 Cases")
    plt.ylabel("Cases (Millions)")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig("covid_report.png")
    print("\nChart saved to: covid_report.png")

# ──────────────────────────────────────────
# RUN THE PIPELINE
# ──────────────────────────────────────────
if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean)
    report()