# 📍 Redpiso Office Scraper: Find Your Next Real Estate Office in Spain! 🇪🇸

Welcome to the Redpiso Office Scraper project! 🏢✨ This Python script is designed to extract details of available real estate offices from the Redpiso website across Spain. Get office addresses, phone numbers, email addresses, and more! 🌟


# 🛠️ Features

- Extract office details: scrapes office data including addresses, phone numbers, and emails.
- Handle cookies: bypass cookie prompts.
- Page navigation: handles pagination to ensure all offices are scraped.
- Data Export: saves collected data in a CSV file for analysis.


# 📦 Requirements

Before running the script, make sure you have the following Python libraries installed:
1. fake-useragent for generating random user agents
2. pandas for data manipulation and saving
3. selenium for browser automation

pip install fake-useragent==1.5.1

pip install pandas==2.2.2

pip install selenium==4.23.1


# 🚀 Getting Started

- Clone the repository:

git clone https://github.com/dsprovider/real_estate_office_scraper.git

cd real_estate_office_scraper

- Run the script:

python real_estate_office_extractor.py

This will scrape office data from the Redpiso website and save it to office_data.csv in your current directory.


# 🧩 How It Works

- Setup: configures a headless Chrome browser with randomized user agents to mimic human behavior. 🕵️‍♂️

- Scraping: navigates through the website, handles cookies, and extracts office details from each page.

- Pagination: clicks through pages to ensure no office is left behind. 📄➡️📄

- Data collection: gathers relevant information and saves it in a CSV file.


# 🛠️ Troubleshooting

- Cookies issue: if the cookie prompt is not handled, ensure the correct element IDs are used or increase wait times.

- Pagination problems: if the script fails to find the 'next' button, check for changes in the site's pagination structure.



# 📜 License

This project is licensed under the MIT License.

