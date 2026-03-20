# Greek Superleague: Panathinaikos FC - Shot Analysis Dashboard

## Overview
A comprehensive football analytics project focused on scraping, processing, and visualizing offensive data for Panathinaikos FC. This repository tracks the relationship between Expected Goals (xG) and actual scoring performance to evaluate finishing quality during the regular season of the 2025-26 Greek Superleague.

## Live Application
The interactive dashboard is deployed and accessible via Streamlit Cloud:
https://panathinaikos-shot-analysis.streamlit.app/

## Project Structure
The repository is organized into a modular structure for better maintainability:
- **`app.py`**: The main entry point for the Streamlit dashboard application.
- **`scripts/`**: Contains the web scraper and the underlying logic for generating plots and filtering data.
- **`data/`**: Stores the raw and processed CSV data (e.g., `pao_full_stats_with_minutes.csv`).
- **`plots/`**: Stores visual outputs produced by the local scripts.

## Key Features & Logic
- **Automated Scraper:** Collects match-specific shot data including coordinates, xG values, and outcomes.
- **Data Filtering:** Specifically excludes `blocked shots` within the processing logic to ensure a more accurate representation of shot conversion and xG efficiency.
- **Minutes Played Tracking:** Calculates player participation time per match or cumulatively to provide context for efficiency metrics.
- **Advanced Visualization:** Utilizing `mplsoccer` for shot maps, heatmaps for threat zones, and dynamic bar charts for efficiency.

## Tech Stack
- **Language:** Python 3.12.6
- **Framework:** Streamlit
- **Libraries:** Pandas, Matplotlib, NumPy, mplsoccer

## Installation & Local Usage
To run the dashboard locally, follow these steps:

1. Clone the repository: git clone https://github.com/antonisraf/Greek-Superleague-Panathinaikos-Shot-Analysis
2. Install the required dependencies: pip install -r requirements.txt
3. Launch the application:streamlit run app.py
