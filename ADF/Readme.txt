Step 1 — Set Up Azure Resources (15 mins)
In the Azure Portal (free tier is fine):

Create a Resource Group: rg-covid-pipeline
Create an Azure SQL Database: covid-db (use Basic tier, ~$5/mo or free trial)
Create a Storage Account → Blob Container named raw-data
Create an Azure Data Factory instance


Step 2 — Python Transform Script (20 mins)
Save this as transform_covid.py and run it locally first:
Install dependencies first:
pip install pandas requests sqlalchemy pyodbc

Step 3 — Query Your Data (5 mins)
In Azure Portal → SQL Database → Query Editor:


Step 4 — Schedule with Azure Data Factory (10 mins)

In ADF → Author → New Pipeline
Add a Web Activity → URL: the CSV link above (just to prove ingestion)
Add a Azure Function or Databricks Notebook activity (or just document that you'd hook your Python script here)
Add a Trigger → Schedule → Daily at 8 AM
