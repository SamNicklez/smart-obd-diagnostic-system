# README.md

## OBD Code Scraper

This Python script is designed to scrape and extract data about On-Board Diagnostic (OBD) trouble codes from the website `https://www.obd-codes.com/`. The script fetches information related to the codes' symptoms and causes, and then stores this data in a CSV file. Original OBD Data taken from `https://github.com/mytrile/obd-trouble-codes/tree/master`

### Prerequisites

Before running the script, ensure you have the following installed:
- Python 3
- `requests` library for Python
- `beautifulsoup4` library for Python

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

### Usage

1. **Data Source CSV**: Prepare a CSV file named `obd-trouble-codes.csv` containing OBD codes and their descriptions. Each row should have a format like: `P0100, Mass or Volume Air Flow Circuit Malfunction`.

2. **CSV File Path**: The script writes the output to a CSV file located at `C:/Users/Samue/Documents/OBDWebscraper/finished_codes.csv`. Ensure this path exists or modify the script to point to your desired output location.

3. **Running the Script**: Execute the script using Python:

```bash
python <script_name>.py
```

### Features

- **Data Scraping**: For each OBD code, the script scrapes the related symptoms and causes from the specified website.
- **Error Handling**: Handles HTTP errors gracefully, outputting 'NA' for unavailable data.
- **CSV Output**: Extracted data is appended to a CSV file with fields: `code`, `description`, `symptoms`, `causes`.

### Functions

- `contains_keywords(tag)`: Checks if a BeautifulSoup tag contains specified keywords.
- `scrape_url(url, desc)`: Scrapes the data for a given OBD code and its description, then writes the information to a CSV file.
- `main()`: Iterates through a list of OBD codes and descriptions, calling `scrape_url` for each.

### Limitations

- The script is tailored to the specific structure of `https://www.obd-codes.com/`. Any changes in the website's layout may require modifications to the script.
- Currently, the script is configured for a specific file path for input and output CSV files. Adjust these paths as necessary for your environment.

### Disclaimer

This script is intended for educational purposes and should be used responsibly.
