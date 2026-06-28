import pandas as pd
import requests
from sqlalchemy import create_engine

# --- EXTRACT ---
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
df = pd.read_csv(url)
print(f"Raw rows: {len(df)}")

# --- TRANSFORM ---
# Select only useful columns
cols = ['iso_code', 'location', 'total_cases', 
        'new_cases', 'total_deaths', 'new_deaths', 
        'total_vaccinations', 'population']
df = df[cols]

# Drop rows where location or total_cases is missing
df = df.dropna(subset=['location', 'total_cases'])

# Fill remaining nulls with 0
df = df.fillna(0)

# Rename columns to snake_case for SQL
df.columns = [c.lower().replace(' ', '_') for c in df.columns]

print(f"Clean rows: {len(df)}")
print(df.head())

# --- LOAD into Azure SQL ---
# Replace with your actual connection string from Azure Portal
server   = "your-server.database.windows.net"
database = "covid-db"
username = "your-admin"
password = "your-password"

conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)

df.to_sql("covid_summary", engine, if_exists="replace", index=False)
print(" Data loaded into Azure SQL!")