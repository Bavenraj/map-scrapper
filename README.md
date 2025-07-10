# map-scrapper
A Python-based scraper to extract business or location data from a map interface for personal research and analysis.

# Maps Data Scraper

This project is a **Python-based web scraper** designed to extract location-based data from a map interface (such as Google Maps). It is built for **educational and personal research purposes**, focusing on gathering structured information about businesses (e.g., fast food chains, restaurants, or other points of interest).

> ⚠️ Note: This tool is intended for **ethical use** only. Please ensure it complies with the terms of service of the site you are scraping.

---

## 🎯 Purpose

The main goal of this project is to:
- Collect structured location data (store names, ratings, reviews, etc.)
- Enable regional or business-specific analysis (e.g., all KFC outlets in Malaysia)
- Automate the repetitive task of manual data collection from map-based search results

---

## 🧩 Features

- 🌍 Scrapes business/store information from Google Maps search results  
- 🏙️ Supports state-level filtering (e.g., only selected Malaysian states)
- ⭐ Extracts key data:
  - Store Name
  - Rating
  - Number of Reviews
  - Operational Status (e.g., Open/Closed)
  - Duration of scraping
- 📁 Saves the output as a structured CSV file
- 🧠 Includes logic to:
  - Avoid duplicates by filtering before writing
  - Handle missing elements gracefully
  - Wait dynamically for elements (using `WebDriverWait`)
- 🔄 Supports repeated runs while keeping the CSV clean

---

## 🛠️ What the Code Consists Of

- `data_extract.py`: Core scraping logic using Selenium + BeautifulSoup
- `states.json`: List of Malaysian states and areas to loop through
- `output.csv`: Final structured dataset (auto-generated)
- Logs and error handling to track scraping progress

---

## 🚀 How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
