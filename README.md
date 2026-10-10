# EVE Online Macroeconomic Inflation & Market Telemetry Analysis

## Project Overview
This repository contains the code and data pipeline for my MBA Capstone research project analyzing macroeconomic inflation and market telemetry within EVE Online's virtual economy.

The project aims to quanitfy regional economic shifts and inflationary pressures by extracting large-scale market telemetry and apply Difference-in-Differences (DiD) statistical anaylses to model regional market shocks and player-driven economic trends.

## Tech Stack
* **Data Processing & ETL** Python, Dask
* **BI / Data Viz:** Power BI
* **Database / Data Warehouse:** PostgreSQL
* **Statistical Analysis / Modeling:** R, SAS Viya
* **Environment:** PC

## Architecture & Pipeline
The workflow is divided into three primary phases:

1. **Extraction & Transformation (Python & Dask):**
   * Combat and market telemetry is ingested from EVE Online & Open Souurce data sources.
   * Dask is utilized for parallel processing and out-of-core computation to handle the massive volume of combat and market transaction logs efficiently.
   * Data is cleaned, normalized, and transformed into a relational schema.

2. **Data Warehousing (PostgreSQL):**
   * The transformed dataset is loaded into a PostgreSQL database, serving as the central repository for historcal data.
   * Queries and materalized views are optimized to feed aggregated regional metrics into the analytical models.
  
3. **Statistical Modeling (R & Sas Viya):**
   * Difference-in-Differeneces (DiD): R scripts pull data from the exported dataset via Power BI matrix to execute DiD analyses, evaluating the causal impact of specific game events or macroeconomic shocks on regional pricing.
   * Advanced Telemetry Modeling: SAS Viya is integrated to run high-performance forecasting and regression models on the inflation data.

## DB Setup
Step-by-step guide on running the db locally:

**Ensure you have pgAdmin installed before running**

1. Create the Target Database (if it doesn't exist)
   ```createdb -U <your_username> -h localhost <your_database_name>```
   
2. Run the table ```creation.sql``` script to configure the tables
   
3. Import the .sql File
   ```psql -U <your_username> -h localhost -d <your_database_name> -f <path/to/db/eve-economy-db.sql>```
