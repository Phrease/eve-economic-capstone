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
