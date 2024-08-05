# Installed Libraries
# pip install fake-useragent==1.5.1
# pip install pandas==2.2.2
# pip install selenium==4.23.1

# Imported Libraries
import os
import time
import random
import pandas as pd

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============= Request Functions ===========================================================================================
   
def sleep_for_random_duration(min_duration=3, max_duration=6):
    sleep_duration = random.uniform(min_duration, max_duration)
    print(f">> Sleeping for {sleep_duration:.2f} seconds...")
    time.sleep(sleep_duration)

# ============= Setup Functions ===============================================================================================

def setup_driver():
    ua = UserAgent()
    random_user_agent = ua.random

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-agent={random_user_agent}')

    # Start the WebDriver and initiate a new browser session
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def accept_cookies_prompt(driver):
    try:
        # Wait for the cookie prompt to appear
        cookie_prompt = WebDriverWait(driver, 6).until(
            EC.visibility_of_element_located((By.ID, "gdpr-cookie-message"))
        )

        # Find the accept button and click on it
        accept_button = cookie_prompt.find_element(By.ID, "gdpr-cookie-accept")
        accept_button.click()

        print(">> Accepted the cookie prompt!")

    except Exception as e:
        print(">> Error occurred while waiting for or handling the cookie prompt:", e)
    

# ============= Parser Functions =======================================================================================

def parse_details_from(office):
    link_href = "<None>"
    address = "<None>"
    phone_number = "<None>"
    email_address = "<None>"

    if office:
        # Office link
        link_element = office.find_element(By.CLASS_NAME, 'item-link')
        if link_element:
            link_href = link_element.get_attribute('href')

        # Office address
        address_element = office.find_element(By.TAG_NAME, 'address')
        if address_element:
            address = address_element.text.replace("\n", " ")

        # Office contact details
        contact_div = office.find_element(By.CLASS_NAME, 'contact')
        if contact_div:
            phone_element = contact_div.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
            if phone_element:
                phone_number = phone_element.text

            email_element = contact_div.find_element(By.CSS_SELECTOR, 'a[href^="mailto:"]')
            if email_element:
                email_address = email_element.text

    data = {
        "link_href": link_href,
        "address": address,
        "phone_number": phone_number,
        "email_address": email_address
    }

    return data

# ============= Scraping Functions ====================================================================================

def scrape_page(driver, collected_data):
    print(f">> Scraping site ... {driver.current_url}")
    offices_list = driver.find_element(By.ID, 'office_list')
    if offices_list:
        for office in offices_list.find_elements(By.TAG_NAME, 'article'):
            office_data = parse_details_from(office)
            office_data['site_link'] = driver.current_url # Add the current URL to the office_data dictionary
            collected_data.append(office_data)

def extract_office_data(url):
    driver = setup_driver()
    collected_data = []  # List to hold all scraped data

    try:
        print(f">> Accessing URL: {url}")
        driver.get(url)
        sleep_for_random_duration(0.5, 1.5)

        accept_cookies_prompt(driver)
        sleep_for_random_duration(0.5, 1.5)

        # --- [A] --- Scrape first page ---
        scrape_page(driver, collected_data)
        sleep_for_random_duration(0.8, 2.3)

        # --- [B] --- Scrape rest of pages recursively ---
        try:
            paginator = driver.find_element(By.CLASS_NAME, 'paginator.pagination')
            if paginator:
                # Locate and click the 'next' page button
                next_page_elem = paginator.find_element(By.CLASS_NAME, 'page-item.next')
                next_page_btn = next_page_elem.find_element(By.TAG_NAME, 'a')

                while next_page_btn:
                    next_page_btn.click()
                    sleep_for_random_duration(0.8, 2.3)

                    # Scrape the current page
                    scrape_page(driver, collected_data)
                    sleep_for_random_duration(0.8, 2.3)

                    # Refresh the paginator element to handle dynamic changes
                    paginator = driver.find_element(By.CLASS_NAME, 'paginator.pagination')
                    try:
                        next_page_disabled_elem = paginator.find_element(By.CLASS_NAME, 'page-item.next.disabled')
                        print(">> Next page button is disabled. Exiting the loop...")
                        print(">> Scraping process finished successfully!")
                        break
                    except Exception as e:
                        print(f">> page-item.next.disabled element yet not found.")
                    
                    next_page_elem = paginator.find_element(By.CLASS_NAME, 'page-item.next')
                    next_page_btn = next_page_elem.find_element(By.TAG_NAME, 'a')

        except Exception as e:
            print(f">> Error detected while navigating pages. Details: {e}")

    except Exception as e:
        print(f">> Error retrieving content from URL: {url}. Details: {e}")
    finally:
        driver.quit()

        # Write collected data to CSV file
        if collected_data:
            df = pd.DataFrame(collected_data)
            outfile_path = os.path.join(os.getcwd(), "office_data.csv")
            df.to_csv(outfile_path, index=False)
            print(">> Data has been written to office_data.csv")

# =============================================================================================================================

def main():
    target_url = "https://www.redpiso.es/oficinas"
    extract_office_data(target_url)


if __name__ == "__main__":
    main()